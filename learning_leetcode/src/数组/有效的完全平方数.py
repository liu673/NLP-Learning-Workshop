# -*- coding: utf-8 -*-

"""
给你一个正整数 num 。如果 num 是一个完全平方数，则返回 true ，否则返回 false 。

完全平方数 是一个可以写成某个整数的平方的整数。换句话说，它可以写成某个整数和自身的乘积。

不能使用任何内置的库函数，如  sqrt 。

示例 1：
输入：num = 16
输出：true
解释：返回 true ，因为 4 * 4 = 16 且 4 是一个整数。

示例 2：
输入：num = 14
输出：false
解释：返回 false ，因为 3.742 * 3.742 = 14 但 3.742 不是一个整数。
"""


class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        left, right = 0, num
        # while left <= right:
        #     middle = left + (right - left) // 2
        #     if middle * middle <= num:
        #         left = middle + 1
        #     else:
        #         right = middle - 1
        # result = left - 1
        # if result * result == num:
        #     return True
        # else:
        #     return False

        while left <= right:
            middle = (left + right) // 2
            if middle * middle == num:
                return True
            elif middle * middle <= num:
                left = middle + 1
            else:
                right = middle - 1
        return False
