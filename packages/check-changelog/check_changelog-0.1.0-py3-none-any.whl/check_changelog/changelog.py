"""
Parse changelog and ensure it conforms to the required structure.

See https://keepachangelog.com/en/ for details
"""

import inspect
import logging
import re

from markdown_it import MarkdownIt

log = logging.getLogger(__name__)
logging.getLogger("markdown_it").setLevel(logging.INFO)


class Tokens(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.idx = 0

    def get(self):
        log.debug("token: %s", self[self.idx])
        return self[self.idx]

    def next(self):  # noqa: A003
        self.idx += 1
        return self.get()

    def is_empty(self):
        return self.idx == len(self)

    def consume_until(self, func):
        log.debug("consume_until")
        while True:
            t = self.get()
            self.next()
            if func(t):
                return


tokens = None


def run(func, narg):
    count = 0
    while True:
        try:
            func()
        except ChangelogError:
            raise
        except Exception:
            if narg == "?" or narg == "*":
                return
            if narg == "+" and count > 0:
                return
            raise
        count += 1
        if narg == "?":
            return
        if isinstance(narg, int) and count == narg:
            return
        if (narg == "+" or narg == "*") and count > len(tokens):
            return


def func_name():
    return inspect.currentframe().f_back.f_code.co_name


tag2type = {
    "h1": "heading",
    "h2": "heading",
    "h3": "heading",
    "ul": "bullet_list",
    "li": "list_item",
    "p": "paragraph",
}


class ChangelogError(Exception):
    def __init__(self, token, msg, msg_extra=""):
        if token.content:
            msg += ": " + token.content
        if msg_extra:
            msg += "; " + msg_extra
        self.message = msg
        self.lineno = token.map[0] if token.map else -1
        self.token = token

    def __str__(self):
        return self.message


def do_item(tag, msg, validate):
    t = tokens.get()
    if not (t.type == tag2type[tag] + "_open" and t.tag == tag):
        raise Exception(msg)
    if validate:
        validate(msg)
    tokens.consume_until(
        lambda x: x.tag == tag
        and x.type == tag2type[tag] + "_close"
        and x.level == t.level
    )


def title():
    log.debug("%s", func_name())
    msg = "expected 'Changelog'"

    def _validate(msg):
        t = tokens.next()
        log.info("title: %s", t.content)
        if t.content != "Changelog":
            raise ChangelogError(t, "bad title", msg)

    do_item("h1", msg, _validate)


def notes():
    log.debug("%s", func_name())
    do_item("p", "", None)


def release_header():
    log.debug("%s", func_name())
    msg = "expected '[Unreleased]' or '[ver] - YYYY-MM-DD'"
    msgr = "expected '[ver] - YYYY-MM-DD'"

    def _validate(msg):
        t = tokens.next()
        log.info("release: %s", t.content)
        kids_no_unreleased = 3
        kids_no_released = 4
        if not (
            len(t.children) >= kids_no_unreleased
            and t.children[0].type == "link_open"
            and t.children[0].attrs.get("href")
        ):
            raise ChangelogError(t, "no link for release")
        rname = t.children[1].content
        log.debug("rname '%s'", rname)
        if rname is None:
            raise ChangelogError(t, "bad release title", msg)

        if rname == "Unreleased":
            if len(t.children) != kids_no_unreleased:
                raise ChangelogError(t, "bad release title", msg)
            return
        if len(t.children) != kids_no_released:
            raise ChangelogError(t, "bad release title", msg)
        rdate = t.children[3].content
        log.debug("rdate '%s'", rdate)
        if not re.search("^ - \\d\\d\\d\\d-\\d\\d-\\d\\d$", rdate):
            raise ChangelogError(t, "bad release date", msgr)

    do_item("h2", msg, _validate)


def change_type():
    log.debug("%s", func_name())
    msg = "expecting '### <Change Type>'"

    def _validate(msg):
        t = tokens.next()
        log.info("change type: %s", t.content)
        msg += "; got '%s'" % t.content
        cnames = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]
        if t.content not in cnames:
            raise ChangelogError(
                t, "bad change type", "expected one of %s" % cnames
            )

    do_item("h3", msg, _validate)


def change_list():
    log.debug("%s", func_name())
    msg = "expecting unordered list"

    def _validate(msg):  # noqa: ARG001
        tokens.next()
        run(change, narg="+")

    do_item("ul", msg, _validate)


def change():
    log.debug("%s", func_name())
    msg = "expecting list item"
    do_item("li", msg, None)


def change_block():
    log.debug("%s", func_name())
    run(change_type, narg=1)
    run(change_list, narg="+")


def release():
    log.debug("%s", func_name())
    run(release_header, narg=1)
    run(notes, narg="*")
    run(change_block, narg="*")


def check_changelog(text):
    log.debug("%s", func_name())
    md = MarkdownIt("commonmark", {"breaks": True, "html": True})
    global tokens  # noqa: PLW0603
    tokens = Tokens(md.parse(text))

    run(title, narg=1)
    run(notes, narg="*")
    run(release, narg="+")

    if tokens.is_empty() or tokens.get().tag == "hr":
        return
    raise ChangelogError(tokens.get(), "out of context")
