DEFAULT_LOCALE = "ru"
SUPPORTED_LOCALES = ("ru", "en")

_TRANSLATIONS: dict[str, dict[str, str]] = {
    "ru": {
        "welcome": (
            "Здравствуйте!\n\n"
            "Спасибо, что обратились в поддержку {org}. Мы всегда готовы помочь "
            "вам с любыми вопросами или проблемами, связанными с использованием "
            "нашего игрового бота.\n\n"
            "Пожалуйста, укажите следующую информацию, чтобы мы могли быстрее "
            "вам помочь:\n"
            "- Описание проблемы или вопроса\n"
            "- Скриншоты или другие подробности, которые могут быть полезны\n\n"
            "Мы стремимся отвечать на все запросы в течение 24 часов. Спасибо "
            "за ваше терпение и понимание.\n\n"
            "С уважением,\n"
            "Команда поддержки {org}"
        ),
        "help": "Просто напишите сообщение — мы создадим тикет и ответим здесь.",
        "language_prompt": "Выберите язык:",
        "language_set": "Язык переключён на русский.",
        "banned": "Вы заблокированы и не можете писать в поддержку.",
    },
    "en": {
        "welcome": (
            "Hello!\n\n"
            "Thank you for contacting {org} support. We're always happy to help "
            "you with any questions or issues related to using our game bot.\n\n"
            "Please provide the following information so we can help you "
            "faster:\n"
            "- Description of the issue or question\n"
            "- Screenshots or other details that might be helpful\n\n"
            "We aim to respond to all requests within 24 hours. Thank you for "
            "your patience and understanding.\n\n"
            "Best regards,\n"
            "{org} Support Team"
        ),
        "help": "Just send a message — we'll create a ticket and reply here.",
        "language_prompt": "Choose your language:",
        "language_set": "Language switched to English.",
        "banned": "You are banned and cannot contact support.",
    },
}


def resolve_locale(locale: str | None) -> str:
    if not locale:
        return DEFAULT_LOCALE

    locale = locale.lower()
    if locale in SUPPORTED_LOCALES:
        return locale

    short = locale.split("-")[0]
    if short in SUPPORTED_LOCALES:
        return short

    return DEFAULT_LOCALE


def t(locale: str, key: str, **kwargs: str) -> str:
    template = _TRANSLATIONS.get(locale, _TRANSLATIONS[DEFAULT_LOCALE])[key]
    return template.format(**kwargs)
