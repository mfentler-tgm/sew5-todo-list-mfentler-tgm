# "Restful ToDo-List"

## Aufgabenstellung
Die detaillierte [Aufgabenstellung](TASK.md) beschreibt die notwendigen Schritte zur Realisierung.

## Implementierung

### CRUD Testen
Um Crud zu testen muss mit curl gearbeitet werden.  
Mit __-X__ kann man die HTTP-Methode angeben.  
Mit __-d__ kann man Daten mitgeben.  
Mit __-H__ kann man einen Header mitgeben.  

Hier ist ein Beispiel um die Post Methode zu testen
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"Task Title","description":"added through curl"}' localhost:5000/
```

## Quellen
