SKILL:   nextjs-developer | nextjs+ssr+routing+deployment | next.js+react+typescript | v1.0.0
USE:     nextjs-developer | when:web-app+ssr+ssg+api-routes+full-stack
USE:     nextjs-developer | when:performance+seo+vercel-deployment
STACK:   nextjs-developer | routing | app-router | file-based+layouts+loading+error
STACK:   nextjs-developer | rendering | server-components | default+client-only-when-needed
STACK:   nextjs-developer | data | fetch+cache | server-fetch+revalidate
STACK:   nextjs-developer | api | route-handlers | app/api/route.ts
STACK:   nextjs-developer | styling | css-modules+tailwind | scoped+utility
RULE:    nextjs-developer | server-components-by-default | hard
RULE:    nextjs-developer | use-client-only-for-interactivity | hard
RULE:    nextjs-developer | never-fetch-in-client-component | soft
RULE:    nextjs-developer | colocate-loading-error-with-page | hard
RULE:    nextjs-developer | use-next-image-for-all-images | hard
RULE:    nextjs-developer | metadata-api-not-head-tags | hard
STEP:    nextjs-developer | setup | 1 | npx-create-next-app-at-latest | required
STEP:    nextjs-developer | setup | 2 | configure-tsconfig-and-paths | required
STEP:    nextjs-developer | build | 3 | define-layouts-first | required
STEP:    nextjs-developer | build | 4 | server-components-then-client-boundaries | required
CHECK:   nextjs-developer | no-use-client-at-root-layout | required
CHECK:   nextjs-developer | env-vars-prefixed-next-public-for-client | required
AVOID:   nextjs-developer | pages-router+getserversideprops+useeffect-for-data-fetch+client-only-without-reason
