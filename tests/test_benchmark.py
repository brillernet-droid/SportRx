from sportrx.benchmark import empty_benchmark_result, get_hybrid_benchmark


def test_benchmark_unavailable_state_works():
    result = empty_benchmark_result()

    assert result["completed"] is False
    assert result["status"] == "Not tested"
    assert result["missing"]


def test_low_equipment_benchmark_path_works():
    result = get_hybrid_benchmark([])

    assert result["available"] is True
    assert result["path"] == "low_equipment"
    assert result["spec"]["label"] == "Prototype benchmark - low-equipment path"


def test_standard_benchmark_path_has_no_validated_cutoffs_claim():
    result = get_hybrid_benchmark(["row", "kettlebell"])

    assert result["path"] == "standard"
    assert result["scoring"]["status"] == "placeholder"
    assert "not validated" in result["scoring"]["note"].lower()
