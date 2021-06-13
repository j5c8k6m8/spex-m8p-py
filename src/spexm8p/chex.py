from spexm8p.token import Token


# 文字集合クラス (Character Expression)
class Chex:
    def __init__(self, chars, include_flg):
        self._char_set = set(chars)
        # self._include_flg => True: include, False: exclude(補集合)
        self._include_flg = True if include_flg else False
        self._len = len(self._char_set)
        if self._len == 0:
            if self._include_flg:
                self._kind = 0  # 空集合
            else:
                self._kind = 1  # 全集合
        else:
            self._kind = 2
        self._str = None  # 遅延評価

    # 空集合確認
    def blank(self):
        if self._kind == 0:
            return True
        else:
            return False

    # 全集合確認
    def whole(self):
        if self._kind == 1:
            return True
        else:
            return False

    # 否定論理演算(~)
    def __invert__(self):
        if self._kind == 2:
            return Chex(self._char_set, not self._include_flg)
        else:
            if self._kind == 0:
                return Chex.WHOLE
            elif self._kind == 1:
                return Chex.BLANK

    # 論理和演算(|)
    def __or__(self, other):
        if self._kind == 2:
            if other._kind == 2:
                if self._include_flg:
                    if other._include_flg:
                        return Chex(self._char_set | other._char_set, True)
                    else:
                        return Chex(other._char_set - self._char_set, False)
                else:
                    if other._include_flg:
                        return Chex(self._char_set - other._char_set, False)
                    else:
                        return Chex(self._char_set & other._char_set, False)
            elif other._kind == 0:
                return self
            elif other._kind == 1:
                return other
        elif self._kind == 0:
            return other
        elif self._kind == 1:
            return self

    # 論理積演算(&)
    def __and__(self, other):
        if self._kind == 2:
            if other._kind == 2:
                if self._include_flg:
                    if other._include_flg:
                        return Chex(self._char_set & other._char_set, True)
                    else:
                        return Chex(self._char_set - other._char_set, True)
                else:
                    if other._include_flg:
                        return Chex(other._char_set - self._char_set, True)
                    else:
                        return Chex(self._char_set | other._char_set, False)
            elif other._kind == 0:
                return other
            elif other._kind == 1:
                return self
        elif self._kind == 0:
            return self
        elif self._kind == 1:
            return other

    # 包含確認
    def include(self, other):
        if self._kind == 2:
            if other._kind == 2:
                if self._include_flg and not other._include_flg:
                    return False
                return (~self & other).blank()
            elif other._kind == 0:
                return True
            elif other._kind == 1:
                return False
        elif self._kind == 0:
            return False
        elif self._kind == 1:
            return True

    def __eq__(self, other):
        if self._kind == other._kind:
            if self._kind != 2:
                return True
            return str(self) == str(other)
        else:
            return False

    def __str__(self):
        if self._str is None:
            if self._kind == 2:
                chars = ''.join(sorted(self._char_set))
                if self._include_flg and self._len == 1:
                    self._str = chars
                else:
                    prefix = '' if self._include_flg else Token.DENY
                    self._str = f'{Token.CH_S}{prefix}{chars}{Token.CH_E}'
            elif self._kind == 0:
                self._str = f'{Token.CH_S}{Token.CH_E}'
            elif self._kind == 1:
                self._str = Token.WHOL
        return self._str

    BLANK = None
    WHOLE = None


Chex.BLANK = Chex([], True)
Chex.WHOLE = Chex([], False)
