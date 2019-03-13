Wagtail + Whatsapp proof of concept
===================================

This is a proof of concept for Wagtail and Whatsapp integration, based on the Wagtail Bakery demo.

**Document contents**

- [Installation](#installation)
- [Next steps](#next-steps)
- [Contributing](#contributing)
- [Other notes](#other-notes)

# Installation

- [Virtualenv](#setup-with-virtualenv)
- [Heroku](#deploy-to-heroku)


Setup with Virtualenv
---------------------

#### Dependencies
* Python 3.4, 3.5 or 3.6
* [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/)
* [VirtualenvWrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) (optional)

### Installation

With [PIP](https://github.com/pypa/pip) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
installed, run:

    mkvirtualenv wagtail-whatsapp-poc --python=python3.6
    python --version

Now we're ready to set up the project itself:

    cd ~/dev [or your preferred dev directory]
    git clone https://github.com/wagtail/wagtail-whatsapp-poc.git
    cd wagtail-whatsapp-poc
    pip install -r requirements/base.txt

Next, we'll set up our local environment variables. We use [django-dotenv](https://github.com/jpadilla/django-dotenv)
to help with this. It reads environment variables located in a file name `.env` in the top level directory of the project. The only variable we need to start is `DJANGO_SETTINGS_MODULE`:

    $ cp bakerydemo/settings/local.py.example bakerydemo/settings/local.py
    $ echo "DJANGO_SETTINGS_MODULE=bakerydemo.settings.local" > .env

To set up your database and load initial data, run the following commands:

    ./manage.py migrate
    ./manage.py load_initial_data
    ./manage.py runserver

Log into the admin with the credentials ``admin / changeme``.

Deploy to Heroku
----------------

You can deploy a demo site to a publicly accessible server with [Heroku's](https://heroku.com)
one-click deployment solution to their free 'Hobby' tier:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/wagtail/wagtail-whatsapp-poc)

If you do not have a Heroku account, clicking the above button will walk you through the steps
to generate one.  At this point you will be presented with a screen to configure your app. For our purposes,
we will accept all of the defaults and click `Deploy`.  The status of the deployment will dynamically
update in the browser. Once finished, click `View` to see the public site.

Log into the admin with the credentials ``admin / changeme``.

To prevent the demo site from regenerating a new Django `SECRET_KEY` each time Heroku restarts your site, you should set
a `DJANGO_SECRET_KEY` environment variable in Heroku using the web interace or the [CLI](https://devcenter.heroku.com/articles/heroku-cli). If using the CLI, you can set a `SECRET_KEY` like so:

    heroku config:set DJANGO_SECRET_KEY=changeme

To learn more about Heroku, read [Deploying Python and Django Apps on Heroku](https://devcenter.heroku.com/articles/deploying-python).

### Storing Wagtail Media Files on AWS S3

If you have deployed the demo site to Heroku or via Docker, you may want to perform some additional setup.  Heroku uses an
[ephemeral filesystem](https://devcenter.heroku.com/articles/dynos#ephemeral-filesystem), and Docker-based hosting
environments typically work in the same manner.  In laymen's terms, this means that uploaded images will disappear at a
minimum of once per day, and on each application deployment. To mitigate this, you can host your media on S3.

This documentation assumes that you have an AWS account, an IAM user, and a properly configured S3 bucket. These topics
are outside of the scope of this documentation; the following [blog post](https://wagtail.io/blog/amazon-s3-for-media-files/)
will walk you through those steps.

This demo site comes preconfigured with a production settings file that will enable S3 for uploaded media storage if
``AWS_STORAGE_BUCKET_NAME`` is defined in the shell environment. All you need to do is set the following environment
variables. If using Heroku, you will first need to install and configure the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli). Then, execute the following commands to set the aforementioned environment variables:

    heroku config:set AWS_STORAGE_BUCKET_NAME=changeme
    heroku config:set AWS_ACCESS_KEY_ID=changeme
    heroku config:set AWS_SECRET_ACCESS_KEY=changeme

Do not forget to replace the `changeme` with the actual values for your AWS account. If you're using a different hosting
environment, set the same environment variables there using the method appropriate for your environment.

Once Heroku restarts your application or your Docker container is refreshed, you should have persistent media storage!

To copy the initial data included with this demo to the S3 bucket (assuming you ran `./manage.py load_initial_data` per
the above), you can use the AWS CLI included with the requirements:

    heroku run aws s3 sync bakerydemo/media/original_images/ s3://<bucket-name>/original_images/

### Note on demo search

Because we can't (easily) use ElasticSearch for this demo, we use Wagtail's native DB search.
However, native DB search can't search specific fields in our models on a generalized `Page` query.
So for demo purposes ONLY, we hard-code the model names we want to search into `search.views`, which is
not ideal. In production, use ElasticSearch and a simplified search query, per
[http://docs.wagtail.io/en/v1.13.1/topics/search/searching.html](http://docs.wagtail.io/en/v1.13.1/topics/search/searching.html).

