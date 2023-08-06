# automates text translation using Deepl Translate

## pip install dtranslate 

## Example Usage

```python
from dtranslate import Dtranslate


textx = r"""Python. was created in the early 1990s by Guido van Rossum at Stichting Mathematisch 
Centrum (CWI, see https://www.cwi.nl/) in the Netherlands as a successor of a 
language called ABC. Guido remains Python’s principal author, although it includes
many contributions from others.
In 1995, Guido. continued his work on Python at the Corporation for 
National Research Initiatives 
(CNRI, see https://www.cnri.reston.va.us/) in Reston, 
Virginia where he released several versions of the software."""


with Dtranslate("en", "de") as go:
    data = go.translate(textx)
print(data)
print(data)
deepl = Dtranslate("en", "de")
translated = deepl.translate(textx)
print(translated)
deepl.quit_translator(soft_kill_first=True)


could not detect version_main.therefore, we are assuming it is chrome 108 or higher
[[('Python. was created in the early 1990s by Guido van Rossum at Stichting Mathematisch Centrum (CWI, see https://www.cwi.nl/) in the Netherlands as a successor of a language called ABC. Guido remains Python’s principal author, although it includes many contributions from others. In 1995, Guido. continued his work on Python at the Corporation for National Research Initiatives (CNRI, see https://www.cnri.reston.va.us/) in Reston, Virginia where he released several versions of the software.', 'Python. wurde in den frühen 1990er Jahren von Guido van Rossum am Stichting Mathematisch Centrum (CWI, siehe https: www.cwi.nl ) in den Niederlanden als Nachfolger einer Sprache namens ABC entwickelt. Guido van Rossum ist nach wie vor der Hauptautor von Python, auch wenn es viele Beiträge von anderen gibt. Im Jahr 1995 setzte Guido seine Arbeit an Python bei der Corporation for National Research Initiatives (CNRI, siehe https: www.cnri.reston.va.us ) in Reston, Virginia fort, wo er mehrere Versionen der Software veröffentlichte.')]]
[[('Python. was created in the early 1990s by Guido van Rossum at Stichting Mathematisch Centrum (CWI, see https://www.cwi.nl/) in the Netherlands as a successor of a language called ABC. Guido remains Python’s principal author, although it includes many contributions from others. In 1995, Guido. continued his work on Python at the Corporation for National Research Initiatives (CNRI, see https://www.cnri.reston.va.us/) in Reston, Virginia where he released several versions of the software.', 'Python. wurde in den frühen 1990er Jahren von Guido van Rossum am Stichting Mathematisch Centrum (CWI, siehe https: www.cwi.nl ) in den Niederlanden als Nachfolger einer Sprache namens ABC entwickelt. Guido van Rossum ist nach wie vor der Hauptautor von Python, auch wenn es viele Beiträge von anderen gibt. Im Jahr 1995 setzte Guido seine Arbeit an Python bei der Corporation for National Research Initiatives (CNRI, siehe https: www.cnri.reston.va.us ) in Reston, Virginia fort, wo er mehrere Versionen der Software veröffentlichte.')]]
could not detect version_main.therefore, we are assuming it is chrome 108 or higher
[[('Python. was created in the early 1990s by Guido van Rossum at Stichting Mathematisch Centrum (CWI, see https://www.cwi.nl/) in the Netherlands as a successor of a language called ABC. Guido remains Python’s principal author, although it includes many contributions from others. In 1995, Guido. continued his work on Python at the Corporation for National Research Initiatives (CNRI, see https://www.cnri.reston.va.us/) in Reston, Virginia where he released several versions of the software.', 'Python. wurde in den frühen 1990er Jahren von Guido van Rossum am Stichting Mathematisch Centrum (CWI, siehe https: www.cwi.nl ) in den Niederlanden als Nachfolger einer Sprache namens ABC entwickelt. Guido van Rossum ist nach wie vor der Hauptautor von Python, auch wenn es viele Beiträge von anderen gibt. Im Jahr 1995 setzte Guido seine Arbeit an Python bei der Corporation for National Research Initiatives (CNRI, siehe https: www.cnri.reston.va.us ) in Reston, Virginia fort, wo er mehrere Versionen der Software veröffentlichte.')]]

```