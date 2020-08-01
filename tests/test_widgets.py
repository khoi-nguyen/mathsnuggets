from mathsnuggets import widgets


def test_widgets():
    test_data = {k: v for k, v in widgets.info.items() if v.get("test")}
    for _name, info in test_data.items():
        form = info["class"](**info["test"])
        form._validate()

        for name, field in form._fields():
            if field.get("computed") or field.get("required"):
                assert getattr(form, name) is not None


def test_generators():
    widget_names = [n for n in dir(widgets) if n[0].isupper() and n[1].islower()]
    for widget in widget_names:
        form = getattr(widgets, widget)()
        if not hasattr(form, "generator"):
            continue

        # Without constraints
        form.generate()
        form._validate()

        for name, _ in form._fields(
            lambda f: f.get("constraint") and not f.get("protected")
        ):
            payload = {}
            payload[name] = True
            form = getattr(widgets, widget)(**payload)
            form.generate()
            form._validate()
