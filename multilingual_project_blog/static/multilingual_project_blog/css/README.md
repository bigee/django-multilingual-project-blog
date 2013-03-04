How to manipulate CSS files
===========================

Which file to edit?
-------------------

It is very simple:

1. Whenever you would like to manipulate one of the variables provided by
   Twitter Bootstrap, open `custom-variables.less` and copy the variable into
   that file and change it's value. Because we import this file right after
   the original `variables.less`, you would effectively override the original
   value and it would become available to all other `.less` files of the
   Bootstrap framework.

2. Whenever you would like to add completely new styles, unrelated to the
   Bootstrap framework, add them to `styles.less` or `responsive-styles.less`.


How to compile the .less files?
-------------------------------

1. Create an RSA key and send your public key to an admin
2. The admin will add your public key to the `authorized_keys` of the `django`
   user on the server.
3. SSH into the server: `ssh django@dev.example.com`
4. Start the filesystem watcher: `watch-less-files.sh`
5. Whenever you change a `.less` file in the project, the `.css` files will
   compiled.


Background
----------

We are using the Twitter Bootstrap CSS Framework for this project. Although
Twitter encourages to manipulate the Bootstrap variables and then download
a `bootstrap.css` file, we don't do that.

We have added the whole Bootstrap repository to this project as a submodule.
Then we have created symlinks to (almost) all of Bootstrap's `.less` files in
the folder `static/css/libs/bootstrap/`.

The trick is, that we did not symlink to the files `bootstrap.less`,
`bootstrap-responsive.less`. These two files import all the other files. We
have created copies of these files in `static/css/` and just slightly edited
them.

What have we done? Right after the import of Bootstrap's `variables.less` we
import our own `custom-variables.less` and at the very end we import our
very own `styles.less`.

Why do we do this? The point of this little trick is to be able to easily
update the Twitter Bootstrap repository whenever there are new versions or
bug fixes (yes! it is full of bugs!). The only way to be able to update easily
is by adding the Bootstrap repository as a submodule and *not* mess around in
their files. When we don't touch Bootstrap's files, we will always be able to
just run `git pull` on the submodule and get the latest version. Since we
placed symlinks in our folders, these latest versions of all the files will
be available to our project immediately.

But of course, we still need to make changes to the Bootstrap variables and add
our own styles. For this reason we added the new files `custom-variables.less`
and `styles.less`.

This means, whenever a new version of Bootstrap is released, we have to do
the following things:

1. Run `git pull` on the submodule
2. Re-create all symlinks in `static/css/libs/bootstrap` because the new
   version might have introduced new files.
3. Compare our copies of `bootstrap.less` and `responsive.less` with the
   originals and see if the new version imports any new files. If so, we need
   to make the same changes in our versions of the files. The safest way is
   to delete our files, make new copies and just insert our two extra lines
   again.


Install lessc on the server
---------------------------

In order to be able to run the lessc command on the server, you need to install
the following things:

    sudo apt-get install rubygems1.8
    sudo gem install rubygems-update
    sudo update_rubygems
    sudo gem install less
    sudo gem install therubyracer
