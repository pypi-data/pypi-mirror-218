# automates text translation using yandex

## pip install yantranslate 

## Example Usage

```python
from yantranslate import Ytranslate


textx = r"""Python. was created in the early 1990s by Guido van Rossum at Stichting Mathematisch 
Centrum (CWI, see https://www.cwi.nl/) in the Netherlands as a successor of a 
language called ABC. Guido remains Python’s principal author, although it includes
many contributions from others.
In 1995, Guido. continued his work on Python at the Corporation for 
National Research Initiatives 
(CNRI, see https://www.cnri.reston.va.us/) in Reston, 
Virginia where he released several versions of the software."""
with Ytranslate("en", "de") as go:
    data = go.translate(textx)
print(data)
print(data)
yandex = Ytranslate("en", "de")
translated = yandex.translate(textx)
print(translated)
yandex.quit_translator(soft_kill_first=True)


could not detect version_main.therefore, we are assuming it is chrome 108 or higher
[[('Python. was created in the early 1990s by Guido van Rossum at Stichting Mathematisch Centrum (CWI, see https://www.cwi.nl/) in the Netherlands as a successor of a language called ABC. Guido remains Python’s principal author, although it includes many contributions from others. In 1995, Guido. continued his work on Python at the Corporation for National Research Initiatives (CNRI, see https://www.cnri.reston.va.us/) in Reston, Virginia where he released several versions of the software.', 'Pythonschlange. wurde Anfang der 1990er Jahre von Guido van Rossum am Stichting Mathematisch Centrum (CWI, siehe https://www.cwi.nl /) in den Niederlanden als Nachfolger einer Sprache namens ABC. Guido bleibt Pythons Hauptautor, obwohl es viele Beiträge von anderen enthält. Im Jahr 1995, Guido. setzte seine Arbeit an Python bei der Corporation for National Research Initiatives (CNRI, siehe) fort https://www.cnri.reston.va.us /) in Reston, Virginia, wo er mehrere Versionen der Software veröffentlichte.')]]
[[('Python. was created in the early 1990s by Guido van Rossum at Stichting Mathematisch Centrum (CWI, see https://www.cwi.nl/) in the Netherlands as a successor of a language called ABC. Guido remains Python’s principal author, although it includes many contributions from others. In 1995, Guido. continued his work on Python at the Corporation for National Research Initiatives (CNRI, see https://www.cnri.reston.va.us/) in Reston, Virginia where he released several versions of the software.', 'Pythonschlange. wurde Anfang der 1990er Jahre von Guido van Rossum am Stichting Mathematisch Centrum (CWI, siehe https://www.cwi.nl /) in den Niederlanden als Nachfolger einer Sprache namens ABC. Guido bleibt Pythons Hauptautor, obwohl es viele Beiträge von anderen enthält. Im Jahr 1995, Guido. setzte seine Arbeit an Python bei der Corporation for National Research Initiatives (CNRI, siehe) fort https://www.cnri.reston.va.us /) in Reston, Virginia, wo er mehrere Versionen der Software veröffentlichte.')]]
could not detect version_main.therefore, we are assuming it is chrome 108 or higher
[[('Python. was created in the early 1990s by Guido van Rossum at Stichting Mathematisch Centrum (CWI, see https://www.cwi.nl/) in the Netherlands as a successor of a language called ABC. Guido remains Python’s principal author, although it includes many contributions from others. In 1995, Guido. continued his work on Python at the Corporation for National Research Initiatives (CNRI, see https://www.cnri.reston.va.us/) in Reston, Virginia where he released several versions of the software.', 'Pythonschlange. wurde Anfang der 1990er Jahre von Guido van Rossum am Stichting Mathematisch Centrum (CWI, siehe https://www.cwi.nl /) in den Niederlanden als Nachfolger einer Sprache namens ABC. Guido bleibt Pythons Hauptautor, obwohl es viele Beiträge von anderen enthält. Im Jahr 1995, Guido. setzte seine Arbeit an Python bei der Corporation for National Research Initiatives (CNRI, siehe) fort https://www.cnri.reston.va.us /) in Reston, Virginia, wo er mehrere Versionen der Software veröffentlichte.')]]

```