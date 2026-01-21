"""
CHOCKER - THE ABSOLUTE MADMAN
============================================
ULTIMATE DISRESPECT MODE

Rules:
1. MUST play en passant if available (holy hell!)
2. MUST stalemate if possible (ultimate troll)
3. When winning (+3): Play WORST move (throw advantage)
4. When losing: Play like 2800 GM
5. Promotion priority: Bishop > Knight > Queen

RAGE MODE:
If opponent doesn't take en passant when available, Chocker goes FULL RAGE
and destroys them with maximum 3000 ELO Stockfish depth 25!
"""

import chess
import chess.engine
import random
import time
from colorama import Fore, Style, init

init(autoreset=True)

class Chocker:
    def __init__(self, stockfish_path="../stockfish/stockfish-windows-x86-64-avx2.exe"):
        import os
        
        # Check if stockfish exists
        if not os.path.exists(stockfish_path):
            print(f"{Fore.RED}ERROR: Stockfish not found at: {stockfish_path}")
            print(f"{Fore.YELLOW}")
            print(f"Please download Stockfish:")
            print(f"1. Go to: https://stockfishchess.org/download/")
            print(f"2. Download Stockfish for Windows")
            print(f"3. Extract to: stockfish/ folder")
            print(f"4. Or update the path in chocker.py line 28")
            print(f"{Fore.RED}")
            raise FileNotFoundError(f"Stockfish not found at {stockfish_path}")
        
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        self.board = chess.Board()
        self.move_count = 0
        self.rage_mode = False
        self.opponent_had_en_passant = False
        self.ultimate_disrespect_mode = True  # Opening disrespect
        self.opening_moves = []  # Track opening moves
        
    def get_evaluation(self):
        """Get current position evaluation"""
        info = self.engine.analyse(self.board, chess.engine.Limit(depth=15))
        score = info["score"].relative
        
        if score.is_mate():
            return 100 if score.mate() > 0 else -100
        return score.score() / 100.0
    
    def get_best_move(self, depth=20):
        """Get the best move (GM mode)"""
        result = self.engine.play(self.board, chess.engine.Limit(depth=depth))
        return result.move
    
    def check_en_passant(self):
        """Check if en passant is available (MUST PLAY IT - HOLY HELL!)"""
        for move in self.board.legal_moves:
            if self.board.is_en_passant(move):
                return move
        return None
    
    def check_opponent_had_en_passant(self):
        """Check if opponent had en passant available on their last turn"""
        # This is checked AFTER opponent moves
        # We need to check if they COULD have played en passant but didn't
        return False  # Will be set by tracking
    
    def check_stalemate_opportunity(self):
        """Check if we can force a stalemate (ultimate troll)"""
        for move in self.board.legal_moves:
            self.board.push(move)
            is_stalemate = self.board.is_stalemate()
            self.board.pop()
            if is_stalemate:
                return move
        return None
    
    def get_worst_move(self):
        """Find the ABSOLUTE WORST move (throws advantage down the drain)"""
        legal_moves = list(self.board.legal_moves)
        
        move_evals = []
        for move in legal_moves:
            self.board.push(move)
            eval_after = -self.get_evaluation()  # Negative because opponent's turn
            self.board.pop()
            move_evals.append((move, eval_after))
        
        # Sort by evaluation (worst first - most negative)
        move_evals.sort(key=lambda x: x[1])
        worst_move = move_evals[0][0]
        
        return worst_move
    
    def should_underpromote(self, move):
        """Check if this is a promotion move"""
        if move.promotion is None:
            return False
        
        piece = self.board.piece_at(move.from_square)
        if piece and piece.piece_type == chess.PAWN:
            to_rank = chess.square_rank(move.to_square)
            if (self.board.turn == chess.WHITE and to_rank == 7) or \
               (self.board.turn == chess.BLACK and to_rank == 0):
                return True
        return False
    
    def check_promotion_stalemate(self, move, promotion_piece):
        """Check if promoting to a specific piece causes stalemate"""
        test_move = chess.Move(move.from_square, move.to_square, promotion=promotion_piece)
        self.board.push(test_move)
        is_stalemate = self.board.is_stalemate()
        self.board.pop()
        return is_stalemate
    
    def get_underpromotion_move(self, move):
        """
        Convert promotion to bishop or knight
        SPECIAL RULE: Promote to queen ONLY if it causes stalemate
        If rook causes stalemate, underpromote instead
        """
        eval_current = self.get_evaluation()
        
        # Check if queen promotion causes stalemate
        queen_stalemates = self.check_promotion_stalemate(move, chess.QUEEN)
        if queen_stalemates:
            # Queen causes stalemate - ULTIMATE DISRESPECT!
            promo_piece = chess.QUEEN
            promo_name = "QUEEN_STALEMATE"
            print(f"{Fore.MAGENTA}[QUEEN STALEMATE] Promoting to queen for stalemate! ULTIMATE DISRESPECT!")
        else:
            # Check if rook causes stalemate
            rook_stalemates = self.check_promotion_stalemate(move, chess.ROOK)
            if rook_stalemates:
                # Rook causes stalemate, but we underpromote instead
                # Choose bishop or knight based on eval
                if eval_current >= 5.0:
                    promo_piece = chess.BISHOP
                    promo_name = "BISHOP"
                else:
                    promo_piece = chess.KNIGHT
                    promo_name = "KNIGHT"
                print(f"{Fore.MAGENTA}[ROOK STALEMATE AVOIDED] Rook would stalemate, underpromotion instead!")
            else:
                # Normal underpromotion logic
                # If we're crushing (+5 or more), always bishop (ultimate disrespect)
                if eval_current >= 5.0:
                    promo_piece = chess.BISHOP
                    promo_name = "BISHOP"
                # If winning comfortably (+3 to +5), knight
                elif eval_current >= 3.0:
                    promo_piece = chess.KNIGHT
                    promo_name = "KNIGHT"
                # Otherwise, random between bishop and knight
                else:
                    promo_piece = random.choice([chess.BISHOP, chess.KNIGHT])
                    promo_name = "BISHOP" if promo_piece == chess.BISHOP else "KNIGHT"
        
        new_move = chess.Move(move.from_square, move.to_square, promotion=promo_piece)
        return new_move, promo_name
    
    def get_ultimate_disrespect_opening(self):
        """
        ULTIMATE DISRESPECT OPENING
        
        As White:
        1. f3 (Fool's Mate setup)
        2. If Black plays d5: g4 (Grob's Attack)
           Else: Kg2 (Bongcloud variation)
        
        As Black:
        1. If White plays d4: f6 (Barnes Defense)
        2. If White plays e4: e5 (normal), then Kg7 (Bongcloud)
           If White doesn't play e4: f6, then g5, NO Kg7
        """
        move_num = len(self.opening_moves)
        
        if self.board.turn == chess.WHITE:
            # White's opening
            if move_num == 0:
                # Move 1: f3 (ULTIMATE DISRESPECT)
                return chess.Move.from_uci("f2f3"), "ultimate_opening"
            elif move_num == 2:
                # Move 2: Check what Black played
                last_black_move = self.opening_moves[-1]
                if last_black_move == "d7d5":
                    # Black played d5, play g4
                    return chess.Move.from_uci("g2g4"), "ultimate_opening"
                else:
                    # Black didn't play d5, play Kf2 (Bongcloud)
                    return chess.Move.from_uci("e1f2"), "ultimate_opening"
        else:
            # Black's opening
            if move_num == 1:
                # Move 1: Check what White played
                last_white_move = self.opening_moves[-1]
                if last_white_move == "d2d4":
                    # White played d4, play f6
                    return chess.Move.from_uci("f7f6"), "ultimate_opening"
                elif last_white_move == "e2e4":
                    # White played e4, play e5 (normal)
                    return chess.Move.from_uci("e7e5"), "ultimate_opening"
                else:
                    # White played something else, play f6
                    return chess.Move.from_uci("f7f6"), "ultimate_opening"
            elif move_num == 3:
                # Move 2 for Black
                first_white_move = self.opening_moves[0]
                if first_white_move == "e2e4" and self.opening_moves[1] == "e7e5":
                    # We played e5 after e4, now play Kf7 (Bongcloud)
                    return chess.Move.from_uci("e8f7"), "ultimate_opening"
                else:
                    # We played f6, now play g5
                    return chess.Move.from_uci("g7g5"), "ultimate_opening"
        
        return None, None
    
    def get_taunt(self, eval_score, move_type):
        """Generate appropriate taunt"""
        if move_type == "ultimate_opening":
            taunts = [
                "[ULTIMATE DISRESPECT] Opening with maximum disrespect!",
                "[FOOL'S MATE SETUP] Let's see if you can punish this!",
                "[BONGCLOUD VARIATION] The most powerful opening!",
                "[GROB'S ATTACK] f3 and g4! Peak chess!",
                "[BARNES DEFENSE] f6! The ultimate defense!",
                "[KING WALK] Moving the king early! What could go wrong?",
                "[ULTIMATE DISRESPECT] This opening is a war crime!"
            ]
        elif move_type == "rage":
            taunts = [
                "[RAGE MODE] YOU DIDN'T TAKE EN PASSANT?! PREPARE TO BE DESTROYED!",
                "[FURY UNLEASHED] No en passant? Time to show you REAL chess!",
                "[MAXIMUM PUNISHMENT] You disrespected en passant. Now you pay!",
                "[3000 ELO ACTIVATED] Ignoring en passant? Death penalty!",
                "[ULTIMATE DISRESPECT] You didn't en passant. I'm ending your career!",
                "[BRICK ON PIPI] No en passant = FULL RAGE MODE! You're done!"
            ]
        elif move_type == "en_passant":
            taunts = [
                "[HOLY HELL!] EN PASSANT IS FORCED! Google en passant!",
                "[BRICK] I MUST play en passant! It's the law!",
                "[ANARCHY CHESS] En passant detected. No choice but to play it!",
                "[FORCED] EN PASSANT! The most powerful move in chess!",
                "[GOOGLE IT] Holy hell! En passant is mandatory!",
                "[BRICK ON PIPI] I see en passant, I play en passant. Simple."
            ]
        elif move_type == "stalemate":
            taunts = [
                "[STALEMATE!] I'm throwing this win! ULTIMATE DISRESPECT!",
                "[DRAW] I was winning but stalemate is funnier!",
                "[TROLL COMPLETE] Stalemating from a winning position. Peak comedy!",
                "[THROW] I could win but where's the fun in that? STALEMATE!",
                "[MADMAN] Forcing a stalemate when I'm up material. I'm insane!",
                "[ULTIMATE DISRESPECT] Stalemate from a winning position!"
            ]
        elif move_type == "worst":
            taunts = [
                "[THROW] That's the WORST move possible. Advantage? Gone!",
                "[BLUNDER] Deliberately throwing my advantage. Can you punish it?",
                "[TRASH] This move is absolute garbage. I'm up +3 though... for now.",
                "[WORST] Literally the worst legal move. Let's see if you capitalize!",
                "[CHOCKER] I'm choking harder than Hikaru in a tournament!",
                "[THROW] Throwing this advantage like it's a hot potato!",
                "[DISASTER] This move is a disaster. But I'm Chocker, what did you expect?",
                "[BLUNDER MASTER] The art of the blunder. Watch and learn!"
            ]
        elif move_type == "bishop":
            taunts = [
                "[BISHOP] BISHOP PROMOTION! ULTIMATE DISRESPECT!",
                "[DISRESPECT] Who needs a queen when you have... a BISHOP?!",
                "[UNDERPROMO] Underpromotion to bishop! Maximum disrespect!",
                "[BISHOP] Bishop > Queen. Fight me.",
                "[FLEX] Promoting to bishop because I can. Still winning.",
                "[CHEF'S KISS] The bishop promotion. Perfection."
            ]
        elif move_type == "knight":
            taunts = [
                "[KNIGHT] KNIGHT PROMOTION! Horsie time!",
                "[UNDERPROMO] Queens are overrated. Knights are where it's at!",
                "[CULTURE] Underpromotion to knight! For the culture!",
                "[KNIGHT] Knight > Queen. This is the way.",
                "[FLEX] Promoting to knight because why not? Still winning.",
                "[HORSIE] Giddy up! Knight promotion activated!"
            ]
        elif move_type == "queen_stalemate":
            taunts = [
                "[QUEEN STALEMATE!] The ONLY time I promote to queen - for stalemate!",
                "[ULTIMATE DISRESPECT] Queen promotion that causes stalemate! Peak comedy!",
                "[STALEMATE QUEEN] Promoting to queen just to draw! Maximum troll!",
                "[QUEEN = STALEMATE] The only acceptable queen promotion!",
                "[TROLL COMPLETE] Queen promotion for stalemate! You can't make this up!",
                "[ULTIMATE DISRESPECT] I promote to queen ONLY to throw the game!"
            ]
        elif move_type == "gm":
            if eval_score < -2:
                taunts = [
                    "[GM MODE] Okay, time to actually try. GM mode activated.",
                    "[SERIOUS] Enough games. Let's cook.",
                    "[TRYHARD] Activating tryhard mode. Watch this.",
                    "[2800 ELO] Time to show you what 2800 ELO looks like.",
                    "[DANGER] Playtime's over. Prepare to suffer."
                ]
            else:
                taunts = [
                    "[SOLID] Solid move. Keeping the pressure.",
                    "[CALCULATED] Calculated. Precise. Deadly.",
                    "[GM] GM move. You're in danger.",
                    "[TEXTBOOK] This is what good chess looks like.",
                    "[WINNING] Textbook. Beautiful. Winning."
                ]
        else:
            taunts = ["[MOVE] Move played."]
        
        return random.choice(taunts)
    
    def make_move(self):
        """Make a move based on evaluation"""
        eval_score = self.get_evaluation()
        
        print(f"\n{Fore.CYAN}Evaluation: {eval_score:+.2f}")
        
        if self.rage_mode:
            print(f"{Fore.RED}[RAGE MODE ACTIVE] MAXIMUM DESTRUCTION!")
        
        move_type = "gm"
        
        # PRIORITY 0: ULTIMATE DISRESPECT OPENING (first 2 moves)
        if self.ultimate_disrespect_mode and len(self.opening_moves) < 4:
            opening_move, opening_type = self.get_ultimate_disrespect_opening()
            if opening_move and opening_move in self.board.legal_moves:
                move = opening_move
                move_type = opening_type
                print(f"{Fore.MAGENTA}[ULTIMATE DISRESPECT OPENING] Maximum disrespect activated!")
            else:
                # Opening move not legal, disable ultimate disrespect
                self.ultimate_disrespect_mode = False
                move = self.get_best_move()
                move_type = "gm"
        
        # PRIORITY 1: EN PASSANT (ALWAYS FORCED!)
        elif self.check_en_passant():
            move = self.check_en_passant()
            move_type = "en_passant"
            print(f"{Fore.MAGENTA}[EN PASSANT DETECTED] MUST PLAY IT! HOLY HELL!")
        
        # RAGE MODE: Override all other rules (except en passant)
        elif self.rage_mode:
            move = self.get_best_move(depth=25)  # MAXIMUM DEPTH
            move_type = "rage"
        
        # PRIORITY 2: STALEMATE (if winning and not in rage mode)
        elif eval_score >= 3.0:
            stalemate_move = self.check_stalemate_opportunity()
            if stalemate_move:
                move = stalemate_move
                move_type = "stalemate"
                print(f"{Fore.MAGENTA}[STALEMATE OPPORTUNITY] THROWING THE WIN! ULTIMATE DISRESPECT!")
            else:
                # Play worst move (throw advantage)
                move = self.get_worst_move()
                move_type = "worst"
        else:
            # Losing or close - play best move
            move = self.get_best_move()
            move_type = "gm"
        
        # Check for underpromotion opportunity (not in rage mode)
        if not self.rage_mode and self.should_underpromote(move):
            move, promo_name = self.get_underpromotion_move(move)
            move_type = promo_name.lower()
        
        # Make the move
        self.board.push(move)
        self.move_count += 1
        
        # Track opening moves
        if len(self.opening_moves) < 4:
            self.opening_moves.append(move.uci())
        
        # Taunt
        taunt = self.get_taunt(eval_score, move_type)
        print(f"{Fore.YELLOW}{taunt}")
        print(f"{Fore.GREEN}Move {self.move_count}: {move}")
        
        return move
    
    def check_opponent_en_passant_miss(self, opponent_move):
        """Check if opponent missed en passant opportunity"""
        # After opponent moves, check if they had en passant available
        # This requires checking the position BEFORE their move
        # For now, we'll implement a simple check
        return False  # Placeholder - would need move history tracking
    
    def play_game(self):
        """Play a full game"""
        print(f"{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}CHOCKER - THE ABSOLUTE MADMAN")
        print(f"{Fore.MAGENTA}ULTIMATE DISRESPECT MODE")
        print(f"{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.CYAN}Opening Strategy:")
        print(f"{Fore.CYAN}  White: 1.f3 then g4 or Kg2 (ULTIMATE DISRESPECT)")
        print(f"{Fore.CYAN}  Black: f6/e5 then g5 or Kg7 (ULTIMATE DISRESPECT)")
        print(f"{Fore.CYAN}")
        print(f"{Fore.CYAN}Game Strategy:")
        print(f"{Fore.CYAN}  - MUST play en passant (holy hell!)")
        print(f"{Fore.CYAN}  - MUST stalemate if possible (ultimate troll)")
        print(f"{Fore.CYAN}  - Winning (+3): Play WORST move (throw advantage)")
        print(f"{Fore.CYAN}  - Losing: Play like 2800 GM")
        print(f"{Fore.CYAN}  - Promotions: Bishop > Knight > Queen")
        print(f"{Fore.RED}  - RAGE MODE: If opponent misses en passant = DESTRUCTION!")
        print(f"{Fore.MAGENTA}{'='*60}\n")
        
        while not self.board.is_game_over():
            print(f"\n{Fore.WHITE}{self.board}")
            print(f"\n{Fore.YELLOW}{'='*60}")
            
            if self.board.turn == chess.WHITE:
                print(f"{Fore.CYAN}Chocker's turn (WHITE):")
                self.make_move()
            else:
                print(f"{Fore.RED}Opponent's turn (BLACK):")
                
                # Check if opponent has en passant available
                opponent_en_passant = self.check_en_passant()
                
                # Opponent plays best move
                opponent_move = self.get_best_move(depth=15)
                self.board.push(opponent_move)
                print(f"{Fore.RED}Opponent plays: {opponent_move}")
                
                # Check if they missed en passant
                if opponent_en_passant and not self.board.is_en_passant(opponent_move):
                    self.rage_mode = True
                    print(f"{Fore.RED}{'='*60}")
                    print(f"{Fore.RED}[RAGE MODE ACTIVATED]")
                    print(f"{Fore.RED}OPPONENT DIDN'T TAKE EN PASSANT!")
                    print(f"{Fore.RED}PREPARE FOR ULTIMATE DISRESPECT!")
                    print(f"{Fore.RED}{'='*60}")
            
            time.sleep(0.5)
        
        # Game over
        print(f"\n{Fore.WHITE}{self.board}")
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}GAME OVER")
        
        result = self.board.result()
        if result == "1-0":
            if self.rage_mode:
                print(f"{Fore.RED}CHOCKER WINS! RAGE MODE SUCCESSFUL! ULTIMATE DISRESPECT!")
            else:
                print(f"{Fore.GREEN}CHOCKER WINS! Despite throwing everything!")
        elif result == "0-1":
            print(f"{Fore.RED}Chocker lost. The throws were too much!")
        else:
            print(f"{Fore.YELLOW}Draw. Probably forced a stalemate. Classic Chocker!")
        
        print(f"{Fore.MAGENTA}{'='*60}")
    
    def close(self):
        """Clean up"""
        self.engine.quit()

def main():
    print(f"{Fore.MAGENTA}CHOCKER - THE ABSOLUTE MADMAN")
    print(f"{Fore.CYAN}ULTIMATE DISRESPECT MODE")
    print(f"{Fore.CYAN}Throws advantages, MUST play en passant, RAGE MODE if you don't!")
    print()
    
    chocker = Chocker()
    
    try:
        chocker.play_game()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Game interrupted!")
    finally:
        chocker.close()

if __name__ == "__main__":
    main()
