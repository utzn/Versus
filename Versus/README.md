# Versus

## Endpoints

### /newgame
* HTTP GET
* Parameters
    * name: Your player name.
    * pin: A passphrase to identify you when issuing commands.
    * id (optional): The game ID. Leave empty when creating a new game, and enter when joining a game.

* Example usage:
    * /newgame?name=Alice&pin=mypin1  
        responds with ab12cd34
        
    * /newgame?id=ab12cd34&name=bob&pin=mypin2  
        responds with 0, indicating success in creating a new game 
