import urllib
from kthread_sleep import sleep
from selenium.webdriver.common.by import By
from translate4colors import Gtranslate


class Ytranslate(Gtranslate):
    def __init__(self, src, dst, headless=True, *args, **kwargs):
        super().__init__(src, dst, headless=headless, *args, **kwargs)

    def _get_google_link(self, s):
        return f"""https://translate.yandex.com/?source_lang={self.src}&target_lang={self.dst}&text={urllib.parse.quote(s)}"""

    def _download(self, text_link, sleeptime, check_percentage):
        self.driver.get(text_link[1])
        sleep(sleeptime)
        _check_percentage = 0
        results = []
        while _check_percentage < check_percentage:
            try:
                for _ in range(10):
                    if len(self.driver.find_elements(By.TAG_NAME, "pre")) >= 1:
                        break
                    sleep(0.5)
                else:
                    raise TimeoutError("Textarea not found...")
                df = self._getdf("span")
                df2 = df.loc[
                    df.aa_outerHTML.str.contains("fullTextTranslation", na=False)
                ]
                translatedtext = df2.aa_innerText.iloc[0]
                lentranslated = len(translatedtext)
                _check_percentage = lentranslated / len(text_link[0]) > check_percentage
                if _check_percentage > check_percentage:
                    results.append((text_link[0], translatedtext))
                    break
            except Exception:
                sleep(1)
                continue
        return results


