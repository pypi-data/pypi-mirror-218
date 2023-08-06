# New algorithm

Assume:
 _tree_ -> the decision tree inducing our original partitioning
 _bounds_ -> a matrix of sorted bounds (_bounds_[i,j] gives the j'th smallest bound on dimension i)
 _L_ -> a mapping from a region id to a tuple of min and max bounds of that region (given as indicies pointing to _bounds_)

init _points_ to be a heap (lexicographically ordered) with only one element, the k-dimensional 0-vector

while _points_ is not empty:

 `p_min` <- _points_.pop()
 `region_id` <- GetRegionId(_tree_, _bounds_,` p_min`)  **note: this requires querying the tree**

 **note: we start with an entire region, to ensure at least 1 one region is processed/removed**
 `p_min`, `p_max` <- _L_(`region_id`)
 `state` <- MakeActualState(_bounds_,` p_min`,` p_max`)
 `action` <- _tree_.predict(`state`)

 if `state` is explored, don't continue, but restart loop
 mark all dimensions as unexhausted

 while some dimensions are still unexhausted:
  `dim` <- choose a random (unexhausted) dimension


## Textual description

Outer while loop:

We start from a minimum point in the partitioning and selects the region at this point.
In future iterations, we choose the starting point as the lexicographically smallest
point in the _points_ list.

Check if this region has been covered by a previous iteration. If so, continue to
next iteration.

Mark all dimensions as unexhausted, and note the action that our current region
maps to. Then, start the inner loop.

Loop for as long as there are unexhausted dimensions:

Choose at random some dimension to expand in. Expanding means to increase 
the value of the upper bound in the given dimension to the value of the next
nearest bound in the same dimension. 

Check if this expanded region overlaps with some regions, that we have already
finished processing in earlier iteration. In that case, undo the expansion and
mark the dimension as exhausted.

Next, get all the regions in the original partitioning, that our current region
overlaps with. Then:
 First, check if any of them maps to a different action, than that of our current
 region. If so, undo the expansion and mark the dimension as exhausted.
 Second, check if any of the regions are split in more than two
