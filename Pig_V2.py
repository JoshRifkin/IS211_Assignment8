# Assignment 8
# By: Joshua Rifkin

import argparse
import random
import time
from itertools import cycle


class Dice(object):
    def __init__(self):
        self.sides = 6

    def rollDie(self):
        return random.randint(1, 6)


class Player(object):
    def __init__(self, name):
        self.playerScore = 0
        self.playerName = name

    def addScore(self, score):
        self.playerScore += score

    def getScore(self):
        return self.playerScore

    def getPlayer(self):
        return self.playerName

    def getType(self):
        return self.playerType


class HumanPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def turn(self, roundScore):
        move = input("\nWhat would you like to do?\n \'r\' = roll\n \'h\' = hold\n")
        return move


class CompPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def turn(self, roundScore):
        totalScore = roundScore + self.getScore()
        if roundScore >= min(25, (100 - totalScore)):
            print(self.getPlayer() + " holds.")
            move = 'h'
        else:
            print(self.getPlayer() + " rolls.")
            move = 'r'
        return move


class PlayerFactory(object):
    def __init__(self, humans, computers):
        self.humanPlayers = humans
        self.compPlayers = computers
        self.playerList = []

    def initPlayers(self):
        for i in range(self.humanPlayers):
            player = HumanPlayer(("Human " + str(i + 1)))
            self.playerList.append(player)
        for i in range(self.compPlayers):
            player = CompPlayer(("Computer " + str(i + 1)))
            self.playerList.append(player)
        return self.playerList


class Game(object):
    def __init__(self):
        self.players = None
        self.playerCycle = None  # cycle(self.players)
        self.turnScore = 0
        self.currPlayer = None

    def newTurn(self):
        return next(self.playerCycle)

    def play(self, humans, computers):
        die = Dice()
        factory = PlayerFactory(humans, computers)
        self.players = factory.initPlayers()
        self.playerCycle = cycle(self.players)

        self.currPlayer = self.newTurn()
        print(self.currPlayer.getPlayer() + "'s turn.")

        while (self.currPlayer.getScore() + self.turnScore) < 100:
            self.turn(die)

        print(self.currPlayer.getPlayer() + " wins! Your score was " +
              str((self.currPlayer.getScore() + self.turnScore)))
        quit()

    def turn(self, die):
        move = self.currPlayer.turn(self.turnScore)

        if move == 'r':
            turn = die.rollDie()
            if turn == 1:
                print(self.currPlayer.getPlayer() + " rolled a 1! End of your turn.")
                self.turnScore = 0
                self.currPlayer = self.newTurn()
                print("\n" + self.currPlayer.getPlayer() + "'s turn.")
            else:
                print("You rolled a " + str(turn))
                self.turnScore += turn
                print("Total round score = " + str(self.turnScore))
                print(self.currPlayer.getPlayer() + "'s total score is: " +
                      str((self.currPlayer.getScore() + self.turnScore)))
        elif move == 'h':
            self.currPlayer.addScore(self.turnScore)
            self.turnScore = 0
            print("End of " + self.currPlayer.getPlayer() + "'s turn.")
            self.currPlayer = self.newTurn()
            print(self.currPlayer.getPlayer() + "'s turn.")
        elif move == 'quit':
            quit()
        else:
            print("Please enter a valid move option.")


class TimedGameProxy(Game):
    def __init__(self):
        Game.__init__(self)
        self.startTime = time.time()
        self.timer = 60

    def play(self, humans, computers):
        die = Dice()
        factory = PlayerFactory(humans, computers)
        self.players = factory.initPlayers()
        self.playerCycle = cycle(self.players)

        self.currPlayer = self.newTurn()
        print(self.currPlayer.getPlayer() + "'s turn.")

        while ((self.currPlayer.getScore() + self.turnScore) < 100) and (time.time() < (self.startTime + self.timer)):
            self.turn(die)

        for player in self.players:
            if player.getScore() > self.currPlayer.getScore():
                self.currPlayer = player

        print(self.currPlayer.getPlayer() + " wins! Your score was " +
              str((self.currPlayer.getScore() + self.turnScore)))
        quit()


def parseArgs(player1, player2):
    comps, humans = 0, 0
    if player1 == 'c':
        comps += 1
    elif player1 == 'h':
        humans += 1
    else:
        print("Player 1 is an invalid player type.\n Please enter 'c' for computer or 'h' for human.")
        quit()
    if player2 == 'c':
        comps += 1
    elif player2 == 'h':
        humans += 1
    else:
        print("Player 2 is an invalid player type.\n Please enter 'c' for computer or 'h' for human.")
        quit()
    return comps, humans


def main():
    parser = argparse.ArgumentParser(description="Which players are human and which are computers?")
    parser.add_argument('-p1', '--player1', type=str, help='What is player 1 "h" - human or "c" - computer?')
    parser.add_argument('-p2', '--player2', type=str, help='What is player 2 "h" - human or "c" - computer?')
    parser.add_argument('-t', '--timed', type=str, help='Is the game timed? True or False?')
    args = parser.parse_args()

    comps, humans = parseArgs(args.player1.lower(), args.player2.lower())

    if args.timed.lower() == 'true':
        game = TimedGameProxy()
        game.play(humans, comps)
    else:
        game = Game()
        game.play(humans, comps)


if __name__ == '__main__':
    main()

