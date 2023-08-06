# easier access to nested lists

## pip install nestedlistops 

## Example Usage

```python
    get_nested_item(l: Iterable, i: Iterable) -> Any
        Retrieves a nested item from a given list or nested list based on the provided index sequence.
        
        Args:
            l (Iterable): The initial list or nested list.
            i (Iterable): An iterable representing the index sequence to access the desired item.
        
        Returns:
            Any: The nested item at the specified index sequence.
        
        Examples:
            >>> from nestedlistops import set_nested_item, get_nested_item
            >>> listas = [[[1, 2], [3, 4]], [[4, 5], [6, 7]], [[7, 8], [9, 9]]]
            >>> get_nested_item(l=listas, i=(0, 1, 0))
            3
    
    
    set_nested_item(l: Iterable, i: Iterable, v: Any)
        Sets the value of a nested item in a given list or nested list based on the provided index sequence.
        
        Args:
            l (Iterable): The initial list or nested list.
            i (Iterable): An iterable representing the index sequence to access the desired item.
            v (Any): The value to be assigned to the nested item.
        
        Returns:
                None (the original iterable is modified)
        
        Examples:
            >>> from nestedlistops import set_nested_item, get_nested_item
            >>> listas = [[[1, 2], [3, 4]], [[4, 5], [6, 7]], [[7, 8], [9, 9]]]
            >>> set_nested_item(l=listas, i=(0, 1, 0), v=1111)
            >>> print(listas)
            [[[1, 2], [1111, 4]], [[4, 5], [6, 7]], [[7, 8], [9, 9]]]
```