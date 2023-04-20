"""Collections of tasks for invoke."""
from invoke import Collection

from tasks import quality, tests


namespace = Collection()
namespace.add_collection(quality)
namespace.add_collection(tests)
