import logging


class _TrainTagFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        format_items = ["[%(asctime)s]", "[%(levelname)-8s]", "%(message)s"]

        # Formatting and appending tags
        tags = record.__dict__.get("tags", None)
        if tags is not None:
            if not isinstance(tags, list):
                tags = [tags]

            formatted_tags = ""
            for tag in tags:
                formatted_tags += f"[{tag}]"

            record.__dict__["formatted_tags"] = formatted_tags
            format_items.append("%(formatted_tags)s")

        self._style._fmt = f'{" ".join(format_items)}'
        return super().format(record)