import urllib
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import undetected_chromedriver as uc
from a_selenium_kill import add_kill_selenium
from textwrapre import wrapre
from kthread_sleep import sleep
from selenium.webdriver.common.by import By
from a_selenium2df import get_df

from retryloop import retryloop


@add_kill_selenium
def get_driver(headless, *args, **kwargs):
    return uc.Chrome(headless=headless, *args, **kwargs)


class Gtranslate:
    r"""
    A class for automating text translation using Google Translate.

    Args:
        src (str): Source language code.
        dst (str): Target language code.
        maxchars (int): Maximum number of characters per translation chunk (default: 4000).
        headless (bool): Whether to run the Chrome browser in headless mode (default: True).
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Attributes:
        src (str): Source language code.
        dst (str): Target language code.
        maxchars (int): Maximum number of characters per translation chunk.
        driver: Selenium WebDriver instance for controlling the Chrome browser.

    Methods:
        translate(text, sleeptime=1, check_percentage=0.5, maxretries=5)
            Translates the given text or list of texts to the target language.

        __str__()
            Returns a string representation of the translation language pair.

        __repr__()
            Returns a string representation of the Gtranslate instance.

        __enter__(*args, **kwargs)
            Called when entering a context management block with the Gtranslate instance.

        __exit__(*args, **kwargs)
            Called when exiting a context management block with the Gtranslate instance.

        quit_translator(soft_kill_first=True)
            Quits the translator by closing the Chrome browser.

    """

    def __init__(self, src, dst, maxchars=4000, headless=True, *args, **kwargs):
        """
        Initialize a Gtranslate instance.

        Args:
            src (str): Source language code.
            dst (str): Target language code.
            maxchars (int): Maximum number of characters per translation chunk (default: 4000).
            headless (bool): Whether to run the Chrome browser in headless mode (default: True).
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        self.src = src
        self.dst = dst
        self.maxchars = maxchars
        self.driver = get_driver(headless=headless, *args, **kwargs)

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

    def __str__(self):
        return f"{self.src} -> {self.dst}"

    def __repr__(self):
        return self.__str__()

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.quit_translator(soft_kill_first=True)

    def _chunk(self, text):
        return wrapre(
            " ".join([g for x in text.splitlines() if (g := x.strip())]),
            blocksize=self.maxchars,
            regexsep=r"\.",
            raisewhenlonger=True,
            removenewlines_from_result=True,
        )

    def _get_google_link(self, s):
        return f"https://translate.google.com/?sl={self.src}&tl={self.dst}&text={urllib.parse.quote(s)}&op=translate"

    def quit_translator(self, soft_kill_first=True):
        self.driver.die_die_die_selenium(soft_kill_first=soft_kill_first)

    def _getdf(
        self,
        q="*",
    ):
        return get_df(
            self.driver,
            By,
            WebDriverWait,
            expected_conditions,
            queryselector=q,
            with_methods=True,
        )

    def _download(self, text_link, sleeptime, check_percentage):
        self.driver.get(text_link[1])
        sleep(sleeptime)
        _check_percentage = 0
        results = []
        while _check_percentage < check_percentage:
            try:
                for _ in range(10):
                    if len(self.driver.find_elements(By.TAG_NAME, "textarea")) > 1:
                        break
                    sleep(0.5)
                else:
                    raise TimeoutError("Textarea not found...")
                df = self._getdf("textarea")
                _check_percentage = (
                    df.iloc[0].aa_textLength / df.iloc[1].aa_textLength
                    > check_percentage
                )
                if _check_percentage > check_percentage:
                    results.append((text_link[0], df.aa_value.iloc[1]))
                    break
            except Exception:
                sleep(1)
                continue
        return results


