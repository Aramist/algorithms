class AVLTree:
    def __init__(self, dataset):
        self.root = None
        self.left = None
        self.right = None
        self.data = None
        self.height = 0
        for data in dataset:
            self.insert(data)

    def insert(self, data):
        """ Returns true if height changed
        Might be more appropriate to split this into a public function (returning
        true for successful insertion) and a private function (returning true for
        tree height update).
        """
        # print(f'Insert {data} into {self.data}')
        if self.data is None:  # Should only trigger for the first insertion
            self.data = data
            self.height = 1
            return False
        if data < self.data:
            if self.left is None:
                self.left = AVLTree([data])
                height_increased = self.right is None  # Height will have changed iff right is None
                self.height += 1 if height_increased else 0
                return True
            else:
                right_height = self.right.height if self.right is not None else 0
                if self.left.insert(data):
                    self.height = max(right_height, self.left.height) + 1
                    self._balance_update()
                    return True
                return False  # Insertion was not performed
        if data > self.data:
            if self.right is None:
                self.right = AVLTree([data])
                height_increased = self.left is None
                self.height += 1 if height_increased else 0
                return True
            else:
                left_height = self.left.height if self.left is not None else 0
                if self.right.insert(data):
                    self.height = max(left_height, self.right.height) + 1
                    self._balance_update()
                    return True
                return False
        else:
            # The data already exists in the tree
            return False

    def delete(self, data):
        pass

    def find(self, data):
        pass

    def _right_rotation(self):
        if self.left is None:
            return
        old_pre = self.left.right

        self.left.right = self.right
        self.right = self.left
        self.left = self.left.left
        self.right.left = old_pre

        # swap data
        temp = self.data
        self.data = self.right.data
        self.right.data = temp

        # Recalc height for self and self.right
        self.right._recalc_height()
        self._recalc_height()

    def _left_rotation(self):
        if self.right is None:
            return
        old_pre = self.left  # Original left child
        old_post = self.right.left  # Original successor (within 2 nodes)
        self.left = self.right
        self.left.left = old_pre
        self.right = self.left.right
        self.left.right = old_post

        temp = self.data
        self.data = self.left.data
        self.left.data = temp

        # Only self and self.left had their children changed, so only they
        # need height updates
        self.left._recalc_height()
        self._recalc_height()

    def _recalc_height(self):
        left_height = self.left.height if self.left is not None else 0
        right_height = self.right.height if self.right is not None else 0
        self.height = max(left_height, right_height) + 1

    def _balance_update(self):
        if self.skew() in (0, 1, -1):
            return
        if self.skew() == 2:
            # If the heavy (right) child has skew of opposite sign, double rotate
            if self.right.skew() < 0:
                self.right._right_rotation()
            self._left_rotation()
        if self.skew() == -2:
            # Again with the heavy children
            if self.left.skew() > 0:
                self.left._left_rotation()
            self._right_rotation()

    def skew(self):
        right_height = self.right.height if self.right is not None else 0
        left_height = self.left.height if self.left is not None else 0
        return right_height - left_height

    def __repr__(self):
        child_elements = [f'{direction}: {a.__repr__()}' for a, direction in zip((self.left, self.right), ('left', 'right'))]
        left_block = '\n  '.join(a for a in child_elements[0].split('\n'))
        right_block = '\n  '.join(a for a in child_elements[1].split('\n'))

        return f'{self.data}, {self.height}, {self.skew()}\n  {left_block}\n  {right_block}'


def avl_demo():
    test_data = [1,2,4,3,8,5,6, -1]
# Without rotations:
#            1
#           / \
#         -1   2
#               \
#                4
#               / \
#              3   8
#                 /
#                5
#                 \
#                  6
    test_tree = AVLTree(test_data)
    print(test_tree)


if __name__ == '__main__':
    avl_demo()

