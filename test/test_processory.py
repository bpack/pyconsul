from pyconsul.processor import divide_list

class TestProcessor:
    def test_divide_list_evenly(self):
        l = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']

        blocks = list(divide_list(l, 3))
        assert len(blocks) == 4

        assert blocks[0] == ['a', 'b', 'c']
        assert blocks[1] == ['d', 'e', 'f']
        assert blocks[2] == ['g', 'h', 'i']
        assert blocks[3] == ['j', 'k', 'l']


    def test_divide_list_unevenly(self):
        l = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
        
        blocks = list(divide_list(l, 5))
        assert len(blocks) == 3
        assert blocks[2] == ['k', 'l']
