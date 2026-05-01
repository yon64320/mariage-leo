# Discours de mariage — Livre interactif style Shrek

Un livre HTML interactif qui simule l'intro de Shrek, à projeter pendant un discours de mariage à plusieurs voix.

## 🤖 Pour Claude Code (premier message à coller)

```
Salut, je reprends un projet en cours. Lis discours-mariage.html et README.md
pour comprendre la structure. C'est un livre HTML interactif style Shrek pour
un discours de mariage à 5 amis. Format livre ouvert : titre+texte à gauche,
photos à droite. 9 spreads au total.

Les photos sont externalisées dans photos/. Liste-moi les 9 spreads avec leur
état actuel et ce qu'il reste à compléter.
```

## 🎯 Quick start

1. Double-clique sur **`discours-mariage.html`** (s'ouvre dans Chrome)
2. Clique "Ouvrir le livre"
3. Appuie sur **`F`** pour le plein écran
4. Navigue avec **`→`** ou clic

## ⌨️ Contrôles

| Touche | Action |
|--------|--------|
| `→` ou `Espace` | Page suivante |
| `←` | Page précédente |
| `M` | Musique on/off |
| `F` | Plein écran |
| `R` | Retour au début |
| `C` | Afficher/masquer les cues scéniques |

Les **cues** sont des notifications rouges en haut à droite qui rappellent au narrateur ce qui se passe à chaque page (qui parle, qui doit arriver en retard, etc). Masquées par défaut, à activer pour les répétitions.

## 📖 Structure du livre

9 spreads (doubles pages). Chaque spread = page de gauche statique avec **titre+texte**, page de droite qui se tourne avec **photos**.

| # | Titre | Contenu actuel | À compléter |
|---|-------|---------------|-------------|
| 1 | Intro | "Il était une fois..." + photo des 5 jeunes + cœur Justine + canyoning/piscine | ✅ |
| 2 | Le miracle | Photo de groupe + screenshots WhatsApp des retards | ✅ |
| 3 | Deux caractères bien marqués | Titre + selfie couple + trio rue | ✅ |
| 4 | Le modèle | Texte + 2 photos couple | ✅ |
| 5 | Arrivée lecteurs 4 et 5 | Texte placeholder | ⚠️ Photos à ajouter |
| 6 | La vraie histoire | Texte placeholder | ⚠️ Photo de groupe à ajouter |
| 7 | Ce que nous savons | Message sincère | ⚠️ Photo des mariés à ajouter |
| 8 | Cérémonie des trophées | Texte + icône 🏆 | ✅ |
| 9 | Fin | "Et ils vécurent heureux" | ⚠️ Photo de mariage à ajouter |

## 🛠️ Modifier le HTML

### Architecture du fichier

```
discours-mariage.html
├── <style>                     # Tout le CSS (ligne ~10 à ~700)
├── <body>
│   ├── .intro                  # Écran d'accueil
│   ├── .cue                    # Notif rouge des cues scéniques
│   ├── .scene > .book
│   │   ├── .left-page-stack    # Page de gauche (statique)
│   │   │   └── #leftContent    # Conteneur dont le HTML est injecté par JS
│   │   └── .right-page-stack   # Pages de droite (qui se tournent)
│   │       ├── SPREAD 1        # ← Une div .right-page par spread
│   │       ├── SPREAD 2
│   │       └── ... (9 au total)
│   ├── .ui                     # Boutons en bas
│   ├── <audio id="bgMusic">    # Musique (vide par défaut)
│   └── <script>                # JS de navigation
```

### Anatomie d'un spread

```html
<!-- ============ SPREAD N: TITRE — DESCRIPTION ============ -->
<div class="right-page"
     data-cue="🎬 SPREAD N - Titre|Instruction scénique pour le narrateur"
     data-left-html='<div class="text-block">...HTML pour la page DE GAUCHE...</div>'
     data-left-pagenum="~ X ~">
  <div class="right-page-front">
    ...HTML pour la page DE DROITE (photos)...
    <div class="page-number">~ Y ~</div>
  </div>
  <div class="right-page-back"></div>
</div>
```

**Important** :
- Le **texte** va dans l'attribut `data-left-html` (sera injecté dans la page de gauche)
- Les **photos** vont dans `<div class="right-page-front">` directement
- Les guillemets simples dans `data-left-html` doivent être encodés `&apos;`

### Classes CSS utilisables

**Pour le texte (page de gauche, dans `data-left-html`)** :
```html
<div class="text-block">
  <div class="chapter-mark">CHAPITRE PREMIER</div>     <!-- Petit caps espacé -->
  <h1>Grand titre</h1>                                  <!-- UnifrakturMaguntia 4-6rem -->
  <h2>Titre moyen</h2>                                  <!-- UnifrakturMaguntia 2-3rem -->
  <p>Texte en italique...</p>
  <div class="ornament">❦ ❦ ❦</div>                    <!-- Séparateur décoratif -->
  <img src="..." class="inline-thumb" alt="">          <!-- Mini photo polaroid -->
</div>
```

**Pour les photos (page de droite)** :
```html
<!-- 1 photo plein cadre -->
<div class="photo-stage single">
  <img src="..." alt="">
</div>

<!-- 2 photos empilées (verticales) -->
<div class="photo-stage">
  <img src="..." alt="">
  <img src="..." alt="">
</div>

<!-- Screenshots WhatsApp (cadre fin) -->
<div class="photo-stage whatsapp">
  <img src="..." alt="">
  <img src="..." alt="">
  <img src="..." alt="">
  <img src="..." alt="">
</div>
```

## 🖼️ Modifier les photos

**Bonne nouvelle** : les photos sont déjà externalisées dans le dossier `photos/`. Tu peux les remplacer directement par d'autres fichiers (en gardant le même nom) ou en référencer de nouvelles dans le HTML.

### Remplacer une photo existante

1. Trouve le nom dans `photos/` (ex: `selfie-couple.jpg`)
2. Mets ton nouveau fichier avec le même nom
3. Recharge le HTML dans le navigateur

### Ajouter une nouvelle photo

1. Mets le fichier dans `photos/` (ex: `photos/ma-nouvelle-photo.jpg`)
2. Dans le HTML, modifie le bon spread pour utiliser `<img src="photos/ma-nouvelle-photo.jpg" alt="">`

### Optimiser une photo (si trop lourde)

Sur Mac avec Python+Pillow installé :
```bash
python tools.py optimize ma-grosse-photo.jpg
# Crée ma-grosse-photo_small.jpg : max 1000px, ~150 KB
```

## 🔧 Photos actuelles

| Nom du fichier | Utilisé sur |
|----------------|-------------|
| `jeunes-cabane.jpg` | Spread 1 (gauche, sous le titre) |
| `justine-portrait.jpg` | Spread 1 (cœur rouge) |
| `groupe-canyoning.jpg` | Spread 1 (droite, haut) |
| `groupe-piscine.jpg` | Spread 1 (droite, bas) |
| `photo-groupe-escape.jpg` | Spread 2 (gauche, sous texte) |
| `whatsapp-1-essayer-etre-a-lheure.jpg` | Spread 2 (droite) |
| `whatsapp-2-jannonce-pas.jpg` | Spread 2 (droite) |
| `whatsapp-3-on-deroge-pas.jpg` | Spread 2 (droite) |
| `whatsapp-4-on-aura-du-retard.jpg` | Spread 2 (droite) |
| `selfie-couple.jpg` | Spread 3 (droite, haut) |
| `trio-rue.jpg` | Spread 3 (droite, bas) |
| `couple-paris-fenetre.jpg` | Spread 4 (gauche, sous texte) |
| `couple-soiree.jpg` | Spread 4 (droite) |

## 🎵 Ajouter de la musique

1. Mets un MP3 dans le même dossier (ex: `musique.mp3`)
2. Dans le HTML, cherche `<audio id="bgMusic" loop>`
3. Décommente la ligne en dessous :
   ```html
   <source src="musique.mp3" type="audio/mpeg">
   ```
4. Dans le livre, appuie sur `M` pour la lancer

Suggestion : "Fairytale" de Smash Mouth (Shrek OST) ou la chanson Disney d'intro pour rappeler les contes.

## 📁 Contenu du dossier

```
mariage-leo-justine/
├── discours-mariage.html        # ← LE FICHIER PRINCIPAL (40 KB)
├── README.md                    # Ce fichier
├── tools.py                     # Utilitaires Python (optimisation, base64)
├── photos/                      # Toutes les photos utilisées dans le livre
│   ├── jeunes-cabane.jpg
│   ├── justine-portrait.jpg
│   ├── groupe-canyoning.jpg
│   ├── groupe-piscine.jpg
│   ├── photo-groupe-escape.jpg
│   ├── couple-paris-fenetre.jpg
│   ├── couple-soiree.jpg
│   ├── selfie-couple.jpg
│   ├── trio-rue.jpg
│   └── whatsapp-1 → 4-...jpg
└── _backup-version-autonome/    # Sauvegarde au cas où
    └── discours-mariage-base64.html  # Version avec images embarquées (1.8 MB)
```

## 💡 Prompts utiles pour Claude Code

```
"Lis le HTML et le README, puis liste-moi les 9 spreads avec leur état"
"Externalise toutes les images base64 vers un dossier photos/"
"Ajoute la photo X au spread N en remplaçant le placeholder"
"Change le texte du spread 5 pour : ..."
"Inverse l'ordre des photos sur le spread 3"
"Ajoute un nouveau spread entre 4 et 5 sur le thème ..."
```

## 🐛 Troubleshooting

- **Musique ne se lance pas** → fichier MP3 manquant ou mal nommé. Le bouton `M` essayera de jouer le `<audio>` qui doit pointer vers un vrai fichier
- **Page blanche** → vérifier la console du navigateur (F12), souvent une erreur JS dans `data-left-html` (guillemets mal échappés)
- **Photo ne s'affiche pas** → si en base64, vérifier qu'il n'y a pas d'espace dans la chaîne ; si externe, vérifier le chemin
- **Animation saccadée** → fermer les autres onglets, le rendu 3D est gourmand

---

Bon mariage 🥂
