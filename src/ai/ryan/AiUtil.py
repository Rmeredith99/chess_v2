import chess

class AiUtil:

    WHITE_WINNING_VAL = 1000
    TIE_VAL = 0
    BLACK_WINNING_VAL = -1000
    
    nodesChecked = 0

    PIECE_VALUE_MAP = {
        chess.QUEEN : 9,
        chess.ROOK : 5,
        chess.KNIGHT : 3,
        chess.BISHOP : 3,
        chess.PAWN : 1
    }

    def minimax(board : chess.Board, depth : int, evalFn, minVal : float = -10000, maxVal : float = 10000) -> float:
        AiUtil.nodesChecked += 1
        if board.is_game_over():
            winner = board.outcome().winner
            if winner == chess.WHITE:
                return AiUtil.WHITE_WINNING_VAL
            elif winner == chess.BLACK:
                return AiUtil.BLACK_WINNING_VAL
            else:
                return AiUtil.TIE_VAL
        elif depth == 0:
            return evalFn(board)

        if (board.turn == chess.WHITE): # if it's a max state
            val = minVal
            for move in AiUtil.getSortedMoves(board):
                board.push(move)
                newVal = AiUtil.minimax(board, depth - 1, evalFn, val, maxVal)
                _ = board.pop()
                if newVal > val:
                    val = newVal
                if val > maxVal:
                    return maxVal
            return val

        else: # if it's a min state
            val = maxVal
            for move in AiUtil.getSortedMoves(board):
                board.push(move)
                newVal = AiUtil.minimax(board, depth - 1, evalFn, minVal, val)
                _ = board.pop()
                if newVal < val:
                    val = newVal
                if val < minVal:
                    return minVal
            return val

    def getSortedMoves(board : chess.Board) -> "list[chess.Move]":
        bestMoves = []
        okMoves = []
        worstMoves = []
        for move in board.legal_moves:
            toPiece = board.piece_at(move.to_square)
            if toPiece != None:
                bestMoves.append(move)
            elif board.is_attacked_by(not board.turn, move.to_square):
                worstMoves.append(move)
            else:
                okMoves.append(move)
        bestMoves.extend(okMoves)
        bestMoves.extend(worstMoves)
        return bestMoves

    def pieceEvaluationScore(board : chess.Board) -> int:
        total = 0
        for pieceType in AiUtil.PIECE_VALUE_MAP:
            total += len(board.pieces(pieceType, chess.WHITE)) * AiUtil.PIECE_VALUE_MAP[pieceType]
            total -= len(board.pieces(pieceType, chess.BLACK)) * AiUtil.PIECE_VALUE_MAP[pieceType]
        return total
