"""Pourquoi une demande a-t-elle echoue ? Le choix des outils, ou la reponse finale ?

    python diagnostic.py qwen3.8-27b__precises

Sans appel reseau : on relit resultats/agent__<etiquette>.json.
"""
import json
import sys


# ---------------------------------------------------------------- a ecrire
def diagnostic(outils_ok, justes):
    cases = {"ok": [], "redaction": [], "outils": [], "detour": []}
    
    for i, (o, j) in enumerate(zip(outils_ok, justes)):
        if o and j:
            cases["ok"].append(i)
        elif o and not j:
            cases["redaction"].append(i)
        elif not o and not j:
            cases["outils"].append(i)
        else:
            cases["detour"].append(i)
            
    return cases

# ---------------------------------------------------------------- fourni
def afficher(r):
    cases = diagnostic(r["outils_ok"], r["justes"])
    print(f"\n{r['etiquette']} : {len(r['ids'])} demandes")
    print(f"\n{'':<17}{'reponse juste':>15}{'reponse fausse':>16}")
    print(f"{'bons outils':<17}{len(cases['ok']):>15}{len(cases['redaction']):>16}")
    print(f"{'mauvais outils':<17}{len(cases['detour']):>15}{len(cases['outils']):>16}")
    for nom in ("outils", "detour", "redaction"):
        if cases[nom]:
            print(f"\n{nom} :")
        for i in cases[nom]:
            print(f"  {r['ids'][i]}  attendu {r['attendus'][i] or '-'}  appele {r['appeles'][i] or '-'}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage : python diagnostic.py qwen3.8-27b__precises")
    with open(f"resultats/agent__{sys.argv[1]}.json", encoding="utf-8") as f:
        afficher(json.load(f))
