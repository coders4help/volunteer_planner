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


def getBraceFormatLogger(name=None, extra=None):
    return BraceFormatLoggerAdapter(getLogger(name=name), extra=extra)


def getLogger(name=None):
    return logging.getLogger(name=name)


if __name__ == "__main__":
    logger = getBraceFormatLogger(__name__, {"logger-extra": "something"})
    logger.error(
        "something {} {extra[extra_key]} {kwargs_key} {extra_key}",
        "postional",
        kwargs_key=123,
        extra={"extra_key": "keyword"},
        stack_info=True,
        exc_info=None,
    )
