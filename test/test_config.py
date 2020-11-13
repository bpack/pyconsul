import pytest
from pyconsul.config import PyconsulConfig

class TestConfig:
    def test_set_properties(self):
        config = PyconsulConfig()
        config.dryrun = True
        config.paths = '/tmp/consul:.'

        assert(config.dryrun == True)
        assert(len(config.paths) == 2)

    def test_str(self):
        config = PyconsulConfig()
        assert(str(config).index('+ dry-run') > 0)
        assert(str(config).index('+ mount-point') > 0)
        assert(str(config).index('+ paths') > 0)
        assert(str(config).index('+ url') > 0)

    def test_validation_missing_url(self):
        config = PyconsulConfig()
        with pytest.raises(RuntimeError):
            config.validate()

