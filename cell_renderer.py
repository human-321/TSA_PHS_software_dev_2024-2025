import sympy
import pylatex

print("sup makai")

def GenerateImageFromLatexString(content):
    doc = pylatex.Document(documentclass="article")
    doc.append(content)
    doc.generate_pdf()


#TODO fix this shit
GenerateImageFromLatexString("x^2")
