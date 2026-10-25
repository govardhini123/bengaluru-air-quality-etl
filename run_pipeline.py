import time
import extract, transform, validate, load

start = time.time()
print("=== Pipeline started ===")

print("[1/4] Extract...")
extract.run()

print("[2/4] Transform...")
transform.run()

print("[3/4] Validate...")
validate.run()

print("[4/4] Load...")
load.run()

print(f"=== Pipeline finished in {time.time() - start:.1f}s ===")