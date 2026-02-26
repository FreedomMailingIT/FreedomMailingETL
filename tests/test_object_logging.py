"""Test logger as an object (suggested by Co-Pilot AI)."""


import pytest
import app_modules.utilities as utils


LM_TYPES = [
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL',
]

# Preperation for tests
utils.initialize_log_file(path=utils.FILE_PATH)


@pytest.mark.parametrize('lm_type', LM_TYPES)
def test_logging_messages(lm_type: str) -> None:
    """Test message sent to logger."""
    msg = f'This is a {lm_type} message.'
    match lm_type:
        case 'DEBUG':
            utils.logger.debug(msg)
        case 'INFO':
            utils.logger.info(msg)
        case 'WARNING':
            utils.logger.warning(msg)
        case 'ERROR':
            utils.logger.error(msg)
        case 'CRITICAL':
            utils.logger.critical(msg)
    _, seg_lines = utils.trim_log_seg(utils.get_last_log_segment())
    assert msg in seg_lines[-1]


if __name__ == '__main__':
    test_logging_messages('INFO')
