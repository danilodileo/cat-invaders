"""pygbag web entry point.

pygbag bundles the whole directory this file lives in and runs it as the
browser app, so it can simply reuse the same async game loop used by the
installable desktop package - no code duplicated between the two builds.

"""

import asyncio

from cat_invaders.main import main

if __name__ == "__main__":
    asyncio.run(main())
