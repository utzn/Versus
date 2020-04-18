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
    * /move?id=ab12cd34&move=e2e4&name=Alice&pin=mypin1  
        responds with  
        | # | a | b | c | d | e | f | g | h |  
        |---|---|---|---|---|---|---|---|---|  
        | 8 | r | n | b | q | k | b | n | r |  
        | 7 | p | p | p | p | p | p | p | p |  
        | 6 | . | . | . | . | . | . | . | . |  
        | 5 | . | . | . | . | . | . | . | . |  
        | 4 | . | . | . | . | P | . | . | . |  
        | 3 | . | . | . | . | . | . | . | . |  
        | 2 | P | P | P | P | . | P | P | P |  
        | 1 | R | N | B | Q | K | B | N | R |
        
    * /move?id=ab12cd34&move=e7e5&name=bob&pin=mypin2  
        responds with  
        | # | a | b | c | d | e | f | g | h |  
        |---|---|---|---|---|---|---|---|---|  
        | 8 | r | n | b | q | k | b | n | r |  
        | 7 | p | p | p | p | . | p | p | p |  
        | 6 | . | . | . | . | . | . | . | . |  
        | 5 | . | . | . | . | p | . | . | . |  
        | 4 | . | . | . | . | P | . | . | . |  
        | 3 | . | . | . | . | . | . | . | . |  
        | 2 | P | P | P | P | . | P | P | P |  
        | 1 | R | N | B | Q | K | B | N | R |
        
        
### /games
* HTTP GET - view a list of all current games on the server
* Return value:
    * A list of all games currently happening on the server.  
      The first player in a game's player list plays as white.
      
### /getboard
* HTTP GET - view an SVG rendering of a particular game
* Parameters
    * id: The game you wish to view.
    
* Return value:
    * An SVG rendering of the game board corresponding to the id parameter.  
      Currently, the website is updated once every second to reflect game updates.

### /delete [TODO]
* HTTP GET - removes an existing game from the server's database
* Parameters
    * id: The game you wish to delete.
    * pin: The pin of either of the players involved in the game.