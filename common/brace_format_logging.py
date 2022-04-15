import logging


class BraceFormatMessage:
    def __init__(self, fmt, *args, **kwargs):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.fmt.format(*self.args, **self.kwargs)


class BraceFormatLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})

    def process(self, msg, kwargs):
        return msg, kwargs

    def log(self, level, msg, /, *args, **kwargs):
        exc_info = kwargs.pop("exc_info", None)
        stack_info = kwargs.pop("stack_info", False)
        stacklevel = kwargs.pop("stacklevel", 1)
        kwargs_extra = kwargs.pop("extra", {})

        extra = {}
        extra.update(self.extra)
        extra.update(kwargs_extra)

        message_kwargs = {"extra": extra}
        message_kwargs.update(extra)
        message_kwargs.update(kwargs)

        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            extra = kwargs.get("extra", {})
            self.logger._log(
                level=level,
                msg=BraceFormatMessage(msg, *args, **message_kwargs),
                args={
                    # not used for actual formatting, but as additional context
                    "args": args,
                    "kwargs": kwargs,
                },
                exc_info=exc_info,
                extra=extra,
                stack_info=stack_info,
                stacklevel=stacklevel,
            )


def getLogger(name=None, extra=None):
    return BraceFormatLoggerAdapter(logging.getLogger(name=name), extra=extra)


if __name__ == "__main__":
    """
    This is for demonstration purpose and to run quick tests.
    """

    class SomeObj:
        some_property = "SomeObj.some_property"

    logger = getLogger(__name__, {"logger-extra": "something"})
    logger.error(
        "something {} {extra[extra_key]} {kwargs_key} {extra_key} {obj.some_property}",
        "postional",
        kwargs_key=123,
        obj=SomeObj,
        extra={"extra_key": "keyword"},
        stack_info=True,
    )
