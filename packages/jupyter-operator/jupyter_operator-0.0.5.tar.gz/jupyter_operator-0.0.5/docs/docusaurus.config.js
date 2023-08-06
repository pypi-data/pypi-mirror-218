/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
  title: 'Ξ 🥷 Jupyter Operator documentation',
  tagline: 'Jupyter Operator documentation',
  url: 'https://clouder.sh',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'datalayer', // Usually your GitHub org/user name.
  projectName: 'datalayer', // Usually your repo name.
  themeConfig: {
    colorMode: {
      defaultMode: 'light',
      disableSwitch: true,
    },
    navbar: {
      title: 'Jupyter Operator Docs',
      logo: {
        alt: 'Datalayer Logo',
        src: 'img/datalayer/logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'index',
          position: 'left',
          label: 'Jupyter Operator',
        },
        {
          href: 'https://github.com/datalayer/clouder',
          position: 'right',
          className: 'header-github-link',
          'aria-label': 'GitHub repository',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Jupyter Operator',
              to: '/docs',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/datalayer',
            },
            {
              label: 'Twitter',
              href: 'https://twitter.com/datalayerio',
            },
            {
              label: 'Linkedin',
              href: 'https://www.linkedin.com/company/datalayer',
            },
          ],
        },
        {
          title: 'More',
          items: [  
            {
              label: 'Datalayer',
              to: 'https://datalayer.io',
            },
            {
              label: 'Blog',
              to: 'https://datalayer.blog',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Datalayer, Inc.`,
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          editUrl:
            'https://github.com/datalayer/clouder/edit/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
