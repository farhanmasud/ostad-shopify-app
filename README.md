# Django Shopify App Starter Kit

> :hourglass_flowing_sand: Under development

Starter kit for Shopify App development with Django
- Uses Django Server Side Rendering approach with the help of [Turbo](https://github.com/hotwired/turbo)
- Uses a [fork](https://github.com/farhanmasud/django-shopify-auth) of [django-shopify-auth](https://github.com/discolabs/django-shopify-auth) with updated [Shopify App Bridge](https://shopify.dev/docs/api/app-bridge) and [Turbo](https://github.com/hotwired/turbo) versions for authentication using sessions
- Takes influence directly from [django-session-token-auth-demo](https://github.com/digismoothie/django-session-token-auth-demo) with a different code structure and tooling
- Uses code structure from [django-tailwind-starter-template](https://github.com/farhanmasud/django-tailwind-starter-template)
- Uses Tailwind ([django-tailwind](https://github.com/timonweb/django-tailwind)) for Styling
- Uses [django-environ](https://django-environ.readthedocs.io/en/latest/) for managing environment variables
- Developer tools -
    - [pip-tools](https://github.com/jazzband/pip-tools) for package management
    - [Black](https://github.com/psf/black) and [pylint](https://github.com/pylint-dev/pylint) for code formatting and linting
    - Bash scripts for quickly setting up the development environment (Currently tested on Ubuntu 22.04 only)

Getting started -

1. Clone repo with your project name `git clone git@github.com:farhanmasud/django-shopify-app-starter-kit.git your-project-name`
2. Setup .env file following the example env file
3. Make all bash scripts executable with `find . -type f -iname "*.sh" -exec chmod +x {} \;`
4. Run `bash update-git-remote.sh` script to remove existing git remote link (of this repo) and update with your on git repo link. Copy your remote URL from GitHub and run the bash script, it'll propmt to enter the new link, paste and hit Enter
5. Setup database [requires step 2] with `bash setup-db.sh`
6. Setup venv and install dependencies with `bash setup-venv-pip-tools.sh`
7. Activate virtual environment with `source venv/bin/activate`
8. Install tailwind dependencies with `python manage.py tailwind install`
9. Run migrations with `python manage.py migrate`
10. Navigate to `static/packages/` directory form your terminal and run `npm install` and `npm run build`
11. Go back to root directory of the project in the terminal and collect static files using `python manage.py collectstatic --no-input`
12. Run the server using `python manage.py runserver`
13. Run ngrok on port 8000
14. Update your app URL on Shopify Partner Account > Your app with your ngrok URL and whitelist `your-ngrok-url/auth/finalize`
15. Install app on your Shopify development store

> :hourglass_flowing_sand: Full documentation coming soon.
