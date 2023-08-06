import urllib

from kthread_sleep import sleep
from retryloop import retryloop
from selenium.webdriver.common.by import By
from translate4colors import Gtranslate


class Dtranslate(Gtranslate):
    def __init__(self, src, dst, headless=True, *args, **kwargs):
        super().__init__(src, dst, headless=headless, *args, **kwargs)

    def _get_google_link(self, s):
        return f'https://www.deepl.com/en/translator#{self.src}/{self.dst}/{urllib.parse.quote(s.replace("/", " "))}'

    def translate(
        self,
        text: list | str,
        sleeptime: float | int = 1,
        check_percentage: float = 0.5,
        maxretries: int = 5,
    ) -> list[tuple[str, str]]:
        """
        Translates the given text or list of texts to the target language.

        Args:
            text (str or list): Text or list of texts to translate.
            sleeptime (float or int): Sleep time between translation requests (default: 1).
            check_percentage (float): Minimum percentage of text translated before considering it complete (default: 0.5).
            maxretries (int): Maximum number of retries for failed translations (default: 5).

        Returns:
            list[tuple]: List of translated text tuples (original, translated).

        """
        if isinstance(text, str):
            splitted_text = self._chunk(text)
        else:
            splitted_text = text
        splitted_text_and_link = [(x, self._get_google_link(x)) for x in splitted_text]
        results = retryloop(
            self._download,
            splitted_text_and_link,
            args=(),
            kwargs={"sleeptime": sleeptime, "check_percentage": check_percentage},
            maxretries=maxretries,
            add_input=True,
            results=True,
            verbose=True,
        )

        return [x[-1] for x in results]

    def _download(self, text_link, sleeptime, check_percentage):
        self.driver.get(text_link[1])
        sleep(sleeptime)
        _check_percentage = 0
        results = []
        while _check_percentage < check_percentage:
            try:
                for _ in range(10):
                    if len(self.driver.find_elements(By.TAG_NAME, "d-textarea")) > 1:
                        break
                    sleep(0.5)
                else:
                    raise TimeoutError("Textarea not found...")
                df = self._getdf("d-textarea")
                _check_percentage = (
                    len(df.aa_innerText.iloc[0]) / len(df.aa_innerText.iloc[1])
                ) > check_percentage
                if _check_percentage > check_percentage:
                    results.append((text_link[0], df.aa_innerText.iloc[1]))
                    break
            except Exception:
                sleep(1)
                continue
        return results

