# -*- coding: utf-8 -*-

"""
给你一个按照非递减顺序排列的整数数组 nums，和一个目标值 target。请你找出给定目标值在数组中的开始位置和结束位置。

如果数组中不存在目标值 target，返回 [-1, -1]。

你必须设计并实现时间复杂度为 O(log n) 的算法解决此问题。

示例 1：
输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]

示例 2：
输入：nums = [5,7,7,8,8,10], target = 6
输出：[-1,-1]

示例 3：
输入：nums = [], target = 0
输出：[-1,-1]
"""
from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        """解法一"""
        # def get_rightborder(nums, target):
        #     left, right = 0, len(nums) -1
        #     rightborder = -3
        #     while left <= right:
        #         middle = left + (right - left) // 2
        #         if nums[middle] > target:
        #             right = middle - 1

        #         else:
        #             left = middle + 1
        #             rightborder = left
        #     return rightborder

        # def get_leftborder(nums, target):
        #     left, right = 0, len(nums) -1
        #     leftborder = -3
        #     while left <= right:
        #         middle = left + (right - left) // 2
        #         if nums[middle] >= target:
        #             right = middle - 1
        #             leftborder = right
        #         else:
        #             left = middle + 1
        #     return leftborder

        # leftborder = get_leftborder(nums, target)
        # rightborder = get_rightborder(nums, target)
        # # print(leftborder, rightborder)

        # if leftborder == -3 or rightborder == -3:
        #     return [-1, -1]
        # if rightborder - leftborder > 1:
        #     return [leftborder+1, rightborder-1]
        # else:
        #     return [-1, -1]

        """解法二"""

        def binarysearch(nums, target):
            left, right = 0, len(nums) - 1
            while left <= right:
                middle = left + (right - left) // 2
                if nums[middle] > target:
                    right = middle - 1
                elif nums[middle] < target:
                    left = middle + 1
                else:
                    return middle
            return -1

        index = binarysearch(nums, target)

        left, right = index, index

        if index == -1:
            return [-1, -1]
        while left - 1 >= 0 and nums[left - 1] == target:
            left -= 1
        while right + 1 < len(nums) and nums[right + 1] == target:
            right += 1
        return [left, right]
