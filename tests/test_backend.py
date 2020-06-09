import mock


def test_init():
    import app

    with mock.patch.object(app.app, "run", return_value=42):
        with mock.patch.object(app, "__name__", "__main__"):
            with mock.patch.object(app.app, "run") as mock_exit:
                app.init()
                assert mock_exit.call_args == mock.call(debug=True, host="0.0.0.0")
