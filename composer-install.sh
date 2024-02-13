#!/usr/bin/sh

composer create-project codeigniter4/appstarter ./www/html/codeigniter
composer create-project symfony/skeleton:"7.0.*" ./www/html/symfony twig/twig
composer create-project laravel/laravel:"11.x-dev" ./www/html/laravel
composer create-project pocketarc/codeigniter ./www/html/codeigniter3
