# Name: Sean Yang
# OSU Email: yangsea@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 2024-06-06
# Description: This code implements a HashMap class with open
#               addressing. This implementation contains methods that like
#               put, resize table, table load, empty buckets, get, contains
#               key, remove, get keys and values, clear, iter, and next.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Update the key/value pair in the hash map. If key already exists,
        the associated value is replaced with new value. If not, both key
        and value is added.
        """
        # Check load factor.
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Update value or add key and value.
        entry = HashEntry(key, value)
        index = self._hash_function(key) % self._capacity
        if self._buckets.get_at_index(index) is None:
            self._buckets.set_at_index(index, entry)
            self._size += 1
        else:
            counter = 0
            while index < self._capacity:
                newIndex = index + counter ** 2
                if newIndex >= self._capacity:
                    newIndex = newIndex % self._capacity
                bucket = self._buckets.get_at_index(newIndex)
                if bucket is None or bucket.is_tombstone:
                    self._buckets.set_at_index(newIndex, entry)
                    self._size += 1
                    return
                if bucket.key == key:
                    bucket.value = value
                    return
                counter += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of table if the new capacity is greater than
        or equal to the current number of elements. If capacity is not a
        prime number, change to next highest prime number.
        """
        # Check if new capacity is valid and change if needed.
        capacity = new_capacity
        if capacity < self._size:
            return
        if not self._is_prime(capacity):
            capacity = self._next_prime(capacity)

        # Change the table capacity.
        tempBuckets = self._buckets
        self._buckets = DynamicArray()
        for i in range(capacity):
            self._buckets.append(None)

        # Reassign values.
        self._size = 0
        oldCapacity = self._capacity
        self._capacity = capacity
        for i in range(oldCapacity):
            entry = tempBuckets.get_at_index(i)
            if entry is not None:
                if not entry.is_tombstone:
                    self.put(entry.key, entry.value)

    def table_load(self) -> float:
        """
        Return the current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets.
        """
        count = 0
        for i in range(self._capacity):
            if (self._buckets.get_at_index(i) is None) or \
                    self._buckets.get_at_index(i).is_tombstone:
                count += 1
        return count

    def get(self, key: str) -> object:
        """
        Return the value associated with the given key. Return None if key
        is not in has map.
        """
        index = self._hash_function(key) % self._capacity
        entry = self._buckets.get_at_index(index)
        counter = 1
        while entry is not None:
            # If match is found
            if entry.key == key and not entry.is_tombstone:
                return entry.value
            # If not probe.
            newIndex = index + counter ** 2
            counter += 1
            if newIndex >= self._capacity:
                newIndex = newIndex % self._capacity
            entry = self._buckets.get_at_index(newIndex)
        return None

    def contains_key(self, key: str) -> bool:
        """
        Return True if key is in hash map and False otherwise.
        """
        if self.get(key) is None:
            return False
        else:
            return True

    def remove(self, key: str) -> None:
        """
        Remove key and value from hash map. If not found, do nothing.
        """
        index = self._hash_function(key) % self._capacity
        entry = self._buckets.get_at_index(index)
        counter = 1
        # Find index for key and remove if found.
        while entry is not None:
            if entry.key == key and not entry.is_tombstone:
                entry.is_tombstone = True
                self._size -= 1
                return
            if entry is None:
                return
            newIndex = index + counter ** 2
            counter += 1
            if newIndex >= self._capacity:
                newIndex = newIndex % self._capacity
            entry = self._buckets.get_at_index(newIndex)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array with tuples of key/value pairs stored
        in the has map.
        """
        da = DynamicArray()
        # Loop through to find buckets that are not empty.
        for i in range(self._capacity):
            entry = self._buckets.get_at_index(i)
            if entry is not None:
                if not entry.is_tombstone:
                    da.append((entry.key, entry.value))
        return da

    def clear(self) -> None:
        """
        Clear the contents of hash map.
        """
        for i in range(self._capacity):
            self._buckets.set_at_index(i, None)
        self._size = 0

    def __iter__(self):
        """
        Enable the hash map to iterate across itself.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Return the next item in a hash map based on location of iterator.
        """
        # Check index.
        if self._index >= self._capacity:
            raise StopIteration

        # Get next
        value = self._buckets.get_at_index(self._index)
        while value is None or value.is_tombstone:
            self._index += 1
            if self._index >= self._capacity:
                raise StopIteration
            value = self._buckets.get_at_index(self._index)
        self._index += 1
        return value

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
