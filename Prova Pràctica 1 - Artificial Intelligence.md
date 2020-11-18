Clara Gubau Gubert - 18070975

# Prova Pràctica 1 - Artificial Intelligence

1. Explica com funciona l'algorisme Depth First Search. Especifica pas per pas com has fet la teva implementació del problema 1 de la pràctica

```python
nodes = util.Stack()
visited = []
nodes.push((problem.getStartState(), []))
while not nodes.isEmpty():
    node = nodes.pop()
    state = node[0]
    movements = node[1]
    if problem.isGoalState(state):
        return movements
   if state not in visited:
    visited.append(state)
    successors = problem.getSuccessors(state)
    for child in successors:
        child_state = child[0]
        child_movements = child[1]
        if child_state not in visited:
            child_action = movements + [child_movements]
            nodes.push((child_state, child_movements))
```

El primer pas és definir les estructures que utilitzarem:

- nodes: un stack on anirem guardant la informació dels diferents nodes. El principal avantatge de l'stack és que l'últim node que entra és el primer que surt. Aquest és un requisit fundamental pel DFS, ja que es tracta de buscar en profunditat i, per tant, el node a expandir 
- visited: una llista que contindrà els nodes utilitzats

Llavors, el següent que hem de fer és afegir el node pel que comencem, que ve donat pel problema quan el cridem (problem.getStartState()). 

El procés que realitzarem es farà mentre encara queden nodes per expandir, és a dir, mentre l'stack nodes no estigui buit (nodes.isEmpty()).

Al fer nodes.pop(), obtenim l'últim node que hem afegit a l'stack. El node, tal i com l'hem definit a la llista nodes, tindrà dos arguments: la posició on es troba o state i la llista de moviments realitzats per arribar a aquell node. Llavors, comprovem si aquest és el node final al que voliem arribar (problem.isGoalState(state)). En cas de que ho sigui, retornem la llista de moviments i ja hem acabat. 

Si ens trobem en el cas que el node extret de l'stack nodes no és el node final, hem de comprovar si ja l'hem expandit, és a dir, si està dins la llista de visited. Si no hi és, l'afegirem i també posarem a l'stack tots els seus successors. 

Els passos següents corresponen al procediment d'afegir a l'stack els nodes sucessors amb la llista de moviments realitzats per arribar-hi. 



2. Defineix què és una heurística. Com funciona l'algorisme A*? Com s'integra l'heurística dins de l'algorisme? Explica la teva implementació específica i justifica la tria d'heurística als problemes 5 i 6 de la práctica.

Una heurística és una estimació dels passos o distància que hi ha des del node actual fins a l'objectiu. 

L'algorisme A* es basa en la idea d'expandir aquells nodes tinguin cost mínim. D'aquesta manera, si l'heurística és correcte, s'expandiran aquells nodes que estan més aprop de l'objectiu o bé que necessiten menys passos per arribar-hi. Cada node obté un cost, donat per la funció d'evaluació:

- f(x) és la funció d'evaluació i correspon al cost estimat de la millor solució que passi pel node x. Es calcula de la següent manera: f(x) = g(x) + h(x)
- g(x) és el cost d'arribar a x des de l'estat inicial
- h(x) és l'heurística, que com hem dit abans, correspon al cost d'arribar a l'objectiu des del node x. 

És amb la funció d'evaluació que integrem l'heurística en l'algorisme A*. 

```python
    nodes = util.PriorityQueue()
    visited = []
    nodes.update((problem.getStartState(), []),  heuristic(problem.getStartState(), problem))
    while not nodes.isEmpty():
        node = nodes.pop()
        state = node[0]
        movements = node[1]

        if problem.isGoalState(state):
            return movements

        if state not in visited:
            visited.append(state)
            successors = problem.getSuccessors(state)
            for child in successors:
                child_state = child[0]
                child_moves = child[1]
                if child_state not in visited:
                    child_moves = movements + [child_moves]
                    cost = problem.getCostOfActions(child_moves)
                    nodes.update((child_state, child_moves), cost + heuristic(child_state, problem))
```

El més important de la implementació és el fet d'utilitzar una cua de prioritat (PriorityQueue()), ja que ens permet ordenar els nodes que anem afegint segons la seva heurística. 

De la mateixa manera que en el DFS, creem una llista dels nodes que anem visitant i actualitzem la cua de prioritat nodes amb l'estat incial i la seva heurística corresponent. Com que es tracta d'una cua de prioritat, haurem d'anar fent update de la cua en comptes de només afegir-lo, ja que cada vegada s'han d'ordenar els nodes segons l'heurística.

Llavors, mentre la cua nodes no estigui buida (while not nodes.isEmpty()) , anirem traient els nodes i comprovarem si aquests son el node final (problem.isGoalState(state)). En el cas que ho sigui, retornem els moviments realitzats per arribar-hi. 

Si no es tracta del node final, comprovem si ja l'hem visitat o encara no. En cas de que no l'haguem afegit fins ara a la llista de visitats, l'afegim i mirem els seus successors. Ara doncs, veiem si els  nodes fills  tampoc han estat visitats i els afegim a la cua de prioritat (nodes) actualitzant la cua amb els moviments corresponents. 

L'heurística que he utilitzat el l'exercici 5 (CornersProblem) ha estat la distància de Manhattan des del corner corresponent fins al node al qual està el pacman. La meva elecció ha estat motivada pel fet que es tracta d'una heurística admisible, consistent i no trivial (ho compleix per definició). 

L'heurística que he utilitzat a l'exercici 6 (FoodSearchProblem), és la que hi ha definida a SearchAgents.py, que correspon a la mazeDistance. Es tracta d'una distància que té en compte les parets de cada problema i calcula la distància que cal recorrer per arribar d'un node a l'altre. És una heurística admisible (per definició, compleix que el valor retornat és menor o igual al cost real d'arribar a aquell node), consistent (també és fàcil comprovar-ho per definició, ja que si hi afegim un node al mig, la distància de l'orgien a l'objectiu és, per força, menor o igual que la distància fins al node intermig més la distància fins l'objectiu) i no trivial (també per definició).



3. Fes un petit esquema que il·lustri la diferència entre l'algorisme Depth First Search i Breadth First Search. Explica la teva implementació de l'algorisme al problema 2 de la pràctica.

|                             BFS                              |                             DFS                              |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| Utilitza una cua (primer que entra és el primer que surt) per trobar el camí més curt fins a l'objectiu | Utilitza un stack (l'últim que entra és el primer que surt) per trobar el camí més curt |
|    Funciona millor per trobar objectius aprop de l'arrel     | Funciona millor per trobar objectius lluny de l'arrel, com ara per trobar solucions a jocs o puzzles |
|                Sempre troba el camí més curt                 | Arriba a la solució pero pot retornar un camí que no sigui el més curt |
| Es tracta d'un algorisme ineficient, ja que expandeix molts més nodes que el DFS | Consta com a algorisme eficient, ja que expandeix menys nodes que el BFS |

```python
    nodes = util.Queue()
    visited = []
    nodes.push((problem.getStartState(), []))

    while not nodes.isEmpty():
        node = nodes.pop()
        state = node[0]
        movements = node[1]

        if problem.isGoalState(state):
            return movements

        if state not in visited:
            visited.append(state)
            successors = problem.getSuccessors(state)
            for child in successors:
                child_state = child[0]
                child_moves = child[1]
                if child_state not in visited:
                    child_moves = movements + [child_moves]
                    nodes.push((child_state, child_moves))
```

Utilitzem una cua per guardar els nodes, una llista de nodes visitats i afegim el primer node. Mentre tinguem nodes per mirar, anem fent el següent procediment:

- Traiem un node i guardem la posició i els moviments per arribar-hi
- Comprovem si és el node final
- Si no ho és, mirem si ja l'hem visitat
  - Si no l'hem visitat, l'afegim a visitats ja que ara l'expandirem
  - Per cada node fill, comprovarem si ja l'hem visitat i l'afegirem a la cua nodes
    - Si no l'hem visitat, actualitzem els moviments per arribar-hi i l'afegim a nodes amb la seva posició i els moviments realitzats

4. Explica què has après amb aquesta pràctica i quin creus tu que és el seu objectiu educatiu. 

Amb aquesta pràctica el principial concepte après ha estat la capacitat de programar un algorisme. És a dir, un cop donat un psedocodi amb unes funcions de python ja programades, ser capaç de escriure el codi de la pràctica. Anteriorment ho havia fet a algorismica, però solien ser exercicis més senzills i amb menys eines ja programades. 

Des del meu punt de vista, seu principal objectiu educatiu és entendre amb més profunditat els algorismes que hem programat i el funcionament de les heurístiques, a part d'aprendre python. 

