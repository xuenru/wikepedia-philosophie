#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.parse import unquote
import ssl

# global variable cache
cache = {}


def getJSON(page):
    params = urlencode({
        'format': 'json',
        'action': 'parse',
        'prop': 'text',
        'redirects': True,
        'page': page})
    API = "https://fr.wikipedia.org/w/api.php"
    # désactivation de la vérification SSL pour contourner un problème sur le
    # serveur d'évaluation -- ne pas modifier
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
    return response.read().decode('utf-8')


def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
        title = parsed['parse']['title']
        content = parsed['parse']['text']['*']
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None


def getPage(page):
    if page in cache:
        title, content = page, cache[page]
        # print(f"{page} is from cache !!!!")
    else:
        title, content = getRawPage(page)
        cache[title] = content
        # print(f"{page} is from API")

    soup = BeautifulSoup(content, 'html.parser')
    links = soup.select('div p a')
    links_10 = []
    i = 0
    for link in links:
        # max 10 page
        if i >= 10:
            break
        href = link.get('href')
        # wiki page
        if href is None or not href.startswith('/wiki/'):
            continue

        # remove prefix /wiki/
        uri = href[6:]

        # remove '#'
        if "#" in uri:
            shape_index = uri.index("#")
            uri = uri[:shape_index]

        # decode
        uri = unquote(uri)

        # replace '_' to space
        uri = uri.replace('_', ' ')

        # check main namespace and avoid duplicate
        if not check_main_namespace(uri) or uri in links_10:
            continue

        # add into target list
        links_10.append(uri)
        i += 1

    return title, links_10


def check_main_namespace(uri):
    """
    check if it's the main namespace page on wikipedia french
    list of namespace: https://fr.wikipedia.org/wiki/Aide:Espace_de_noms
    :param uri:
    :return:
    """
    if ":" in uri:
        colon_index = uri.index(":")
        prefix = uri[:colon_index]
        return prefix not in ['Média', 'Spécial', 'Discussion', 'Utilisateur', 'Discussion utilisateur', 'Wikipédia',
                              'Discussion Wikipédia', 'Fichier', 'Discussion fichier', 'MediaWiki',
                              'Discussion MediaWiki', 'Modèle', 'Discussion modèle', 'Aide', 'Discussion aide',
                              'Catégorie', 'Discussion catégorie']

    return True


if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    print("Ça fonctionne !")

    # Voici des idées pour tester vos fonctions :
    # print(getJSON("Utilisateur:A3nm/INF344"))
    # print(getRawPage("Utilisateur:A3nm/INF344"))
    # print(getRawPage("Histoire"))
