from datalab.utils import *


class Vector:
    @overload
    def __init__(
        self,
        size: int,
        dtype: type = int,
        fill: Union[int, float, str, bool] = 0,
    ) -> None:
        """Initializes a vector with the specified size, data type, and fill value.

        Parameters
        ----------
        size : int
            Size of the vector.
        dtype : type, optional
            Data type of the vector elements. Default is int.
        fill : int or float or str or bool, optional
            Value used to fill the vector. Default is 0"""

        pass

    @overload
    def __init__(self, object: Iterable) -> None:
        """Initializes a vector from an iterable object.

        Parameters
        ----------
        object : Iterable
            Iterable object containing the data for the vector"""
        pass

    def __init__(
        self,
        arg1: Optional[Union[Iterable, int]],
        dtype: Optional[type] = int,
        fill: Optional[Union[int, float, str, bool]] = 0,
    ) -> None:
        if isinstance(arg1, int):
            self.__size = arg1
            self.__dtype = dtype
            self._initialize_data_structure(size=arg1, dtype=dtype, fill=fill)

        else:
            self._initialize_data_structure(object=arg1)

        self.__supported_types = int, float, str, bool
        self.__precision = 4

    def __str__(self) -> str:
        buffer = [" " for _ in range(self.size)]

        for i, value in enumerate(self.__data):
            if self.dtype == float:
                splited_value = str(value).split(".")

                if len(splited_value) == 1:
                    if splited_value[0] == "0":
                        formatted_value = f"0."

                    else:
                        formatted_value = f"{splited_value[0]}."

                if len(splited_value) == 2:
                    if splited_value[0] == "0" and splited_value[1] == "0":
                        formatted_value = f"0."

                    elif splited_value[0] == "0" and splited_value[1] != "0":
                        if len(splited_value[1]) > self.__precision:
                            formatted_value = "{:.{}e}".format(value, self.__precision)
                        else:
                            formatted_value = f"0.{splited_value[1]}"

                    elif splited_value[0] != "0" and splited_value[1] == "0":
                        formatted_value = f"{splited_value[0]}."

                    else:
                        if len(splited_value[1]) > self.__precision:
                            formatted_value = "{:.{}e}".format(value, self.__precision)
                        else:
                            formatted_value = f"{splited_value[0]}.{splited_value[1]}"

            elif self.dtype == int:
                formatted_value = str(value)

            elif self.dtype == bool:
                formatted_value = str(value)

            else:
                formatted_value = f"'{str(value)}'"

            buffer[i] = formatted_value

        max_element_length = max(len(str(item)) for item in buffer)

        output = "\n"

        for value in buffer:
            output += f"│ {value}{' ' * (max_element_length - len(value) + 1)}│\n"

        return output

    def __add__(self, element: Iterable) -> Self:
        buffer = self.copy()

        def vector_addition(A: Iterable, B: Iterable) -> Iterable:
            return [a + b for a, b in zip(A, B)]

        if isinstance(element, Vector):
            if buffer.size == element.size:
                buffer.__data = vector_addition(buffer.__data, element)
            else:
                raise ArithmeticError("Cannot add vectors with different sizes")

        elif isinstance(element, (list, tuple)):
            if len(element) != buffer.size:
                raise ArithmeticError("Cannot add vectors with different sizes")

            buffer.__data = vector_addition(buffer.__data, element)

        else:
            raise ValueError("You can only add vector to another vector, list or tuple")

        return buffer

    def __sub__(self, element: Iterable) -> Self:
        buffer = self.copy()

        def vector_subtraction(A: Iterable, B: Iterable) -> Iterable:
            return [a - b for a, b in zip(A, B)]

        if isinstance(element, Vector):
            if buffer.size == element.size:
                buffer.__data = vector_subtraction(buffer.__data, element)
            else:
                raise ArithmeticError("Cannot subtract vectors with different sizes")

        elif isinstance(element, (list, tuple)):
            if len(element) != buffer.size:
                raise ArithmeticError("Cannot subtract vectors with different sizes")

            buffer.__data = vector_subtraction(buffer.__data, element)

        else:
            raise ValueError(
                "You can only subtract a vector from another vector, list or tuple"
            )

        return buffer

    def __mul__(self, element: Iterable) -> Self:
        buffer = self.copy()

        if isinstance(element, Vector):
            if buffer.size != element.size:
                raise ArithmeticError("Cannot multiply vectors with different sizes")

            buffer.__data = [a * b for a, b in zip(buffer.__data, element.__data)]

        elif isinstance(element, (list, tuple)):
            if buffer.size != len(element):
                raise ArithmeticError("Cannot multiply vectors with different sizes")

            buffer.__data = [a * b for a, b in zip(buffer.__data, element)]

        elif isinstance(element, (int, float, str, bool)):
            buffer.__data = [element * a for a in buffer.__data]

        else:
            raise ValueError("Invalid operand for vector multiplication")

        return buffer

    def __pow__(self, exponent: int) -> Self:
        buffer = self.copy()

        if not isinstance(exponent, int):
            raise ValueError(
                "Vector exponentiation is only supported for integer exponents"
            )

        if exponent < 0:
            raise ValueError(
                "Vector exponentiation is not supported for negative exponents"
            )

        if exponent == 0:
            return Vector(buffer.size, dtype=buffer.dtype, fill=1)

        for _ in range(exponent - 1):
            buffer *= self

        return buffer

    def __setitem__(self, index: int, value: Union[int, float, str, bool]) -> None:
        if not isinstance(index, int):
            raise ValueError("Index value must be an integer")

        for supported_type in self.__supported_types:
            if self.dtype == supported_type:
                self.__data[index] = supported_type(value)
                break

    def __getitem__(self, index: int) -> Union[int, float, str, bool]:
        if not isinstance(index, int):
            raise ValueError("Index value must be an integer")

        return self.__data[index]

    def _empty_element(self) -> Union[int, float, str, bool]:
        if self.dtype == float:
            return 0.0

        elif self.dtype == str:
            return ""

        elif self.dtype == bool:
            return False

        else:
            return 0

    def _estimate_data_type(self, object: Iterable) -> type:
        type_counts = {int: 0, float: 0, str: 0, bool: 0}

        for element in object:
            if isinstance(element, int):
                type_counts[int] += 1
            elif isinstance(element, float):
                type_counts[float] += 1
            elif isinstance(element, str):
                type_counts[str] += 1
            elif isinstance(element, bool):
                type_counts[bool] += 1

        if type_counts[int] > 0 and type_counts[float] > 0:
            return float
        else:
            return max(type_counts, key=type_counts.get)

    def _fill_data(
        self,
        object: Optional[Iterable] = None,
        fill: Optional[Union[int, float, str, bool]] = None,
    ) -> None:
        empty_element = self._empty_element() if fill is None else fill

        self.__data = [empty_element for _ in range(self.size)]

        if object is not None:
            for i, element in enumerate(object):
                try:
                    self.__data[i] = element
                except IndexError:
                    self.__data[i] = empty_element

    def _initialize_data_structure(
        self,
        object: Optional[Iterable] = None,
        size: Optional[int] = None,
        dtype: Optional[type] = None,
        fill: Optional[Union[int, float, str, bool]] = None,
    ) -> None:
        if object is not None:
            self.__size = len(object)
            self.__dtype = self._estimate_data_type(object)

            self._fill_data(object=object, fill=fill)

        elif size is not None:
            self.__size = size
            self.__dtype = dtype

            self._fill_data(fill=fill)

        else:
            raise ValueError(
                "Matrix._initilize_data_structure() has recived wrong parameters"
            )

    def _adjust_size(self) -> None:
        buffer = self.__data.copy()

        init_item = self._empty_element()

        self.__data = [init_item for _ in range(self.size)]

        for i in range(self.size):
            try:
                self.__data[i] = buffer[i]
            except:
                continue

    def _change_data_type(self, new_dtype: type) -> None:
        if new_dtype not in self.__supported_types:
            raise ValueError(
                f"dl.Vector.dtype must take one of this value: {self.__supported_types}"
            )
        self.__data = list(map(new_dtype, self.__data))

    @property
    def size(self) -> int:
        """Vector's length (number of elements)"""
        return self.__size

    @size.setter
    def size(self, new_size: int) -> None:
        if isinstance(new_size, int):
            self.__size = new_size
            self._adjust_size()
        else:
            raise ValueError("Vector size must be an integer")

    @property
    def dtype(self) -> type:
        """Store element's current type"""

        return self.__dtype

    @dtype.setter
    def dtype(self, new_value: type) -> None:
        if new_value in (int, float, str, bool):
            self.__dtype = new_value
        else:
            raise ValueError("`dl.Vector.dtype` property must be an type object")

    def fill(self, value: Union[int, float, str, bool]) -> Self:
        """Fills the vector with the specified value.

        Parameters
        ----------
        value : int or float or str or bool
            Value to fill the vector with"""

        if not has_same_type(self.dtype, value):
            value = convert(value, self.dtype)

        for i in range(self.size):
            self.__data[i] = value

        return self

    def change_dtype(self, new_dtype: type) -> Self:
        """Changes the data type of the vector.

        Parameters
        ----------
        new_dtype : type
            The new data type for the vector"""

        self.dtype = new_dtype
        self._change_data_type(new_dtype)

        return self

    def set_precision(self, new_precision: int) -> None:
        """Sets the precision for numerical values in the vector.

        Parameters
        ----------
        new_precision : int
            The new precision value to set for numerical values.

        Raises
        ------
        ValueError
            If the provided precision is not an integer"""

        if isinstance(new_precision, int):
            self.__precision = new_precision
        else:
            raise ValueError("Number precision must be an integer")

    def to_list(self) -> list[Union[int, float, str, bool]]:
        """Converts the vector to a Python list"""

        return self.__data

    def to_tuple(self) -> tuple[Union[int, float, str, bool]]:
        """Converts the vector to a Python tuple"""

        return tuple(self.__data)

    def copy(self) -> Self:
        """Creates a copy of the vector"""

        return copy.copy(self)

    def deep_copy(self) -> Self:
        """Creates a deep copy of the vector"""

        return copy.deepcopy(self)
