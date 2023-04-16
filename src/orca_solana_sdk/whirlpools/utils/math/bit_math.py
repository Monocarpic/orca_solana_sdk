class BitMath:
    @staticmethod
    def mul(n0: int, n1: int, limit: int) -> int:
        result = n0 * n1
        if BitMath.is_over_limit(result, limit):
            raise OverflowError(f"Mul result higher than {limit}")
        return result

    @staticmethod
    def mul_div(n0: int, n1: int, d: int, limit: int) -> int:
        return BitMath.mul_div_round_up_if(n0, n1, d, False, limit)

    @staticmethod
    def mul_div_round_up_if(
        n0: int, n1: int, d: int, round_up: bool, limit: int
    ) -> int:
        if not d:
            raise ZeroDivisionError("mul_div denominator is zero")

        p = BitMath.mul(n0, n1, limit)
        n = p / d

        if round_up:
            return n + 1 if p % d > 0 else n
        else:
            return n

    @staticmethod
    def is_over_limit(n0: int, limit: int):
        return n0 > pow(2, limit) - 1
