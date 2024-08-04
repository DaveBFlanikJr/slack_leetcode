from db_service import DatabaseBuilder, get_database
from fastapi import Depends


# Testing the DB connection 

leetcode_solution = {
    "problem_number": 1,
    "problem_name": "two-sum",
    "code": """# frozen_string_literal: true

# 1. Two Sum
# https://leetcode.com/problems/two-sum

# @param {Integer[]} nums
# @param {Integer} target
# @return {Integer[]}
def two_sum(nums, target)
  h = {}
  (0..nums.size - 1).each do |i|
    complement = target - nums[i]

    return [i, h[complement]] if h.key?(complement)

    h[nums[i]] = i
  end
end

# **************** #
#       TEST       #
# **************** #

require "test/unit"
class Test_two_sum < Test::Unit::TestCase
  def test_
    assert_equal [0, 1].sort, two_sum([2, 7, 11, 15], 9).sort
    assert_equal [1, 2].sort, two_sum([3, 2, 4], 6).sort
    assert_equal [0, 1].sort, two_sum([3, 3], 6).sort
  end
end
"""
}

def test_insert_solution(db: DatabaseBuilder = Depends(get_database)):
    if db:
        db.init_db()
        db.insert_solution(
            leetcode_solution["problem_number"],
            leetcode_solution["problem_name"],
            leetcode_solution["code"]
        )
        print("Solution entered into db successfully.")
        # Ensure the engine is disposed
        db.engine.dispose()
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    # Manually call the function with the dependency injection
    test_insert_solution(db=get_database())