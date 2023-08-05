import atexit
import logging
from typing import Any, Awaitable, Callable, Dict, List, Optional

from motion.execute import Executor
from motion.route import Route
from motion.utils import DEFAULT_KEY_TTL, configureLogging, logger


def is_logger_open(logger: logging.Logger) -> bool:
    for handler in logger.handlers:
        if (
            hasattr(handler, "stream")
            and handler.stream is not None
            and not handler.stream.closed
        ):
            return True
    return False


class ComponentInstance:
    def __init__(
        self,
        component_name: str,
        instance_name: str,
        init_state_func: Optional[Callable],
        init_state_params: Optional[Dict[str, Any]],
        save_state_func: Optional[Callable],
        load_state_func: Optional[Callable],
        infer_routes: Dict[str, Route],
        fit_routes: Dict[str, List[Route]],
        logging_level: str = "WARNING",
        disabled: bool = False,
    ):
        """Creates a new instance of a Motion component.

        Args:
            name (str):
                Name of the component we are creating an instance of.
            instance_name (str):
                Name of the instance we are creating.
            logging_level (str, optional):
                Logging level for the Motion logger. Uses the logging library.
                Defaults to "WARNING".
        """
        self._component_name = component_name
        configureLogging(logging_level)
        # self._serverless = serverless
        # indicator = "serverless" if serverless else "local"
        logger.info(f"Creating local instance of {self._component_name}...")
        atexit.register(self.shutdown)

        # Create instance name
        self._instance_name = instance_name

        self.running = False
        self.disabled = disabled
        self._executor = Executor(
            self._instance_name,
            init_state_func=init_state_func,
            init_state_params=init_state_params if init_state_params else {},
            save_state_func=save_state_func,
            load_state_func=load_state_func,
            infer_routes=infer_routes,
            fit_routes=fit_routes,
            disabled=self.disabled,
        )
        self.running = True

    @property
    def instance_name(self) -> str:
        """Component name with a random phrase to represent
        the name of this instance.
        In the form of componentname__randomphrase.
        """
        return self._instance_name

    @property
    def instance_id(self) -> str:
        """Latter part of the instance name, which is a random phrase
        or a user-defined ID."""
        return self._instance_name.split("__")[-1]

    def shutdown(self) -> None:
        """Shuts down a Motion component instance, saving state.
        Automatically called when the instance is garbage collected.

        Usage:
        ```python
        from motion import Component

        C = Component("MyComponent")

        @C.init_state
        def setUp():
            return {"value": 0}

        # Define infer and fit operations

        if __name__ == "__main__":
            c_instance = C()
            c_instance.run(...)
            c_instance.run(...)
            c_instance.shutdown()
        ```
        """
        if self.disabled:
            return

        if not self.running:
            return

        is_open = is_logger_open(logger)

        if is_open:
            logger.info(f"Shutting down {self._instance_name}...")

        self._executor.shutdown(is_open=is_open)

        self.running = False

    def get_version(self) -> int:
        """
        Gets the state version (might be outdated) currently being
        used for infer ops.

        Usage:
        ```python
        from motion import Component

        C = Component("MyComponent")

        @C.init_state
        def setUp():
            return {"value": 0}

        # Define infer and fit operations

        if __name__ == "__main__":
            c_instance = C()
            c_instance.get_version() # Returns 1 (first version)
        ```
        """
        return self._executor.version  # type: ignore

    def update_state(self, state_update: Dict[str, Any]) -> None:
        """Writes the state update to the component instance's state.
        If a fit op is currently running, the state update will be
        applied after the fit op is finished. Warning: this could
        take a while if your fit op takes a long time!

        Usage:
        ```python
        from motion import Component

        C = Component("MyComponent")

        @C.init_state
        def setUp():
            return {"value": 0}

        # Define infer and fit operations
        ...

        if __name__ == "__main__":
            c_instance = C()
            c_instance.read_state("value") # Returns 0
            c_instance.update_state({"value": 1, "value2": 2})
            c_instance.read_state("value") # Returns 1
            c_instance.read_state("value2") # Returns 2
        ```

        Args:
            state_update (Dict[str, Any]): Dictionary of key-value pairs
                to update the state with.
        """
        self._executor._updateState(state_update)

    def read_state(self, key: str) -> Any:
        """Gets the current value for the key in the component instance's state.

        Usage:
        ```python
        from motion import Component

        C = Component("MyComponent")

        @C.init_state
        def setUp():
            return {"value": 0}

        # Define infer and fit operations
        ...

        if __name__ == "__main__":
            c_instance = C()
            c_instance.read_state("value") # Returns 0
            c_instance.run(...)
            c_instance.read_state("value") # This will return the current value
            # of "value" in the state
        ```

        Args:
            key (str): Key in the state to get the value for.

        Returns:
            Any: Current value for the key.
        """
        return self._executor._loadState()[key]

    def flush_fit(self, dataflow_key: str) -> None:
        """Flushes the fit queue corresponding to the dataflow
        key, if it exists, and updates the instance state.
        Warning: this is a blocking operation and could take
        a while if your fit op takes a long time!

        Example Usage:
        ```python
        from motion import Component

        C = Component("MyComponent")

        @C.init_state
        def setUp():
            return {"value": 0}

        @C.infer("add")
        def add(state, value):
            return state["value"] + value

        @C.fit("add")
        def add(state, value, infer_result):
            return {"value": state["value"] + value}

        @C.infer("multiply")
        def multiply(state, value):
            return state["value"] * value

        if __name__ == "__main__":
            c = C() # Create instance of C
            c.run("add", kwargs={"value": 1})
            c.flush_fit("add") # (1)!
            c.run("add", kwargs={"value": 2}) # This will use the updated state

        # 1. Waits for the fit op to finish, then updates the state
        ```

        Args:
            dataflow_key (str): Key of the dataflow.

        Raises:
            RuntimeError: If the component instance was initialized to
            be disabled.
        """
        if self.disabled:
            raise RuntimeError("Cannot run a disabled component instance.")

        self._executor.flush_fit(dataflow_key)

    def run(
        self,
        # *,
        dataflow_key: str,
        kwargs: Dict[str, Any] = {},
        cache_ttl: int = DEFAULT_KEY_TTL,
        ignore_cache: bool = False,
        force_refresh: bool = False,
        flush_fit: bool = False,
    ) -> Any:
        """Runs the dataflow (infer and fit ops) for the keyword argument
        passed in. If the key is not found to have any ops, an error
        is raised. Only one dataflow key should be passed in.

        Example Usage:
        ```python
        from motion import Component

        C = Component("MyComponent")

        @C.init_state
        def setUp():
            return {"value": 0}

        @C.infer("add")
        def add(state, value):
            return state["value"] + value

        @C.fit("add")
        def add(state, value, infer_result):
            return {"value": state["value"] + value}

        if __name__ == "__main__":
            c = C() # Create instance of C
            c.run("add", kwargs={"value": 1}, flush_fit=True) # (1)!
            c.run("add", kwargs={"value": 1}) # Returns 1
            c.run("add", kwargs={"value": 2}, flush_fit=True) # (2)!

            c.run("add", kwargs={"value": 3})
            time.sleep(3) # Wait for the previous fit op to finish

            c.run("add", kwargs={"value": 3}, force_refresh=True) # (3)!

        # 1. Waits for the fit op to finish, then updates the state
        # 2. Returns 2, result state["value"] = 4
        # 3. Force refreshes the state before running the dataflow, and
        #    reruns the infer op even though the result might be cached.
        ```


        Args:
            dataflow_key (str): Key of the dataflow to run.
            kwargs (Dict[str, Any]): Keyword arguments to pass into the
                dataflow ops, in addition to the state.
            cache_ttl (int, optional):
                How long the inference result should live in a cache (in
                seconds). Defaults to 1 day (60 * 60 * 24).
            ignore_cache (bool, optional):
                If True, ignores the cache and runs the infer op. Does not
                force refresh the state. Defaults to False.
            force_refresh (bool, optional): Read the latest value of the
                state before running an inference call, otherwise a stale
                version of the state or a cached result may be used.
                Defaults to False.
            flush_fit (bool, optional):
                If True, waits for the fit op to finish executing before
                returning. If the fit queue hasn't reached batch_size
                yet, the fit op runs anyways. Force refreshes the
                state after the fit op completes. Defaults to False.

        Returns:
            Any: Result of the inference call. Might take a long time
            to run if `flush_fit = True` and the fit operation is
            computationally expensive.
        """
        if self.disabled:
            raise RuntimeError("Cannot run a disabled component instance.")

        infer_result = self._executor.run(
            key=dataflow_key,
            kwargs=kwargs,
            cache_ttl=cache_ttl,
            ignore_cache=ignore_cache,
            force_refresh=force_refresh,
            flush_fit=flush_fit,
        )

        return infer_result

    async def arun(
        self,
        # *,
        dataflow_key: str,
        kwargs: Dict[str, Any] = {},
        cache_ttl: int = DEFAULT_KEY_TTL,
        ignore_cache: bool = False,
        force_refresh: bool = False,
        flush_fit: bool = False,
    ) -> Awaitable[Any]:
        """Async version of run. Runs the dataflow (infer and fit ops) for the
        specified key.

        Example Usage:
        ```python
        from motion import Component
        import asyncio

        C = Component("MyComponent")

        @C.infer("sleep")
        async def sleep(state, value):
            await asyncio.sleep(value)
            return "Slept!"

        async def main():
            c = C()
            await c.arun("sleep", kwargs={"value": 1})

        if __name__ == "__main__":
            asyncio.run(main())
        ```

        Args:
            dataflow_key (str): Key of the dataflow to run.
            kwargs (Dict[str, Any]): Keyword arguments to pass into the
                dataflow ops, in addition to the state.
            cache_ttl (int, optional):
                How long the inference result should live in a cache (in
                seconds). Defaults to 1 day (60 * 60 * 24).
            ignore_cache (bool, optional):
                If True, ignores the cache and runs the infer op. Does not
                force refresh the state. Defaults to False.
            force_refresh (bool, optional): Read the latest value of the
                state before running an inference call, otherwise a stale
                version of the state or a cached result may be used.
                Defaults to False.
            flush_fit (bool, optional):
                If True, waits for the fit op to finish executing before
                returning. If the fit queue hasn't reached batch_size
                yet, the fit op runs anyways. Force refreshes the
                state after the fit op completes. Defaults to False.
            **kwargs:
                Keyword arguments for the infer and fit ops. You can only
                pass in one pair.

        Raises:
            ValueError: If more than one dataflow key-value pair is passed.
            RuntimeError: If the component instance was initialized to
            be disabled.

        Returns:
            Awaitable[Any]: Awaitable Result of the inference call.
        """
        if self.disabled:
            raise RuntimeError("Cannot run a disabled component instance.")

        infer_result = await self._executor.arun(
            key=dataflow_key,
            kwargs=kwargs,
            # value=value,
            cache_ttl=cache_ttl,
            ignore_cache=ignore_cache,
            force_refresh=force_refresh,
            flush_fit=flush_fit,
        )  # type: ignore

        return infer_result  # type: ignore
