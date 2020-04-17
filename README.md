# Versus

## Endpoints

### /newgame
* HTTP GET - create a new game
* Parameters
    * name: Your player name.
    * pin: A passphrase to identify you when issuing commands.
    * id (optional): The game ID. Leave empty when creating a new game, and enter when joining a game.

* Return value:
    * A unique game identifier, or
    * 0, if you are the second player to join a game.

* Example usage:
    * /newgame?name=Alice&pin=mypin1  
        responds with ab12cd34
        
    * /newgame?id=ab12cd34&name=bob&pin=mypin2  
        responds with 0, indicating success in creating a new game 
        
### /move
* HTTP GET - make a move in an existing game
* Parameters
    * id: The game you wish to make a move in.
    * move: Your move in extended algebraic notation (e.g. moving the white pawn from e2 to e4 -> e2e4)
    * name: Your player name.
    * pin: A passphrase to identify you when issuing commands (see /newgame).

* Return value:
    * A graphical board representation

* Example usage:
    * /newgame?id=ab12cd34&move=e2e4name=Alice&pin=mypin1  
        responds with  
        | a | b | c | d | e | f | g | h |  
        |---|---|---|---|---|---|---|---|  
        | r | n | b | q | k | b | n | r |  
        | p | p | p | p | p | p | p | p |  
        | . | . | . | . | . | . | . | . |  
        | . | . | . | . | . | . | . | . |  
        | . | . | . | . | p | . | . | . |  
        | . | . | . | . | . | . | . | . |  
        | P | P | P | P | . | P | P | P |  
        | R | N | B | Q | K | B | N | R |
        
    * /newgame?id=ab12cd34&name=bob&pin=mypin2  
        responds with 0, indicating success in creating a new game 
        
        
### /games
* HTTP GET - view a list of all current games on the server