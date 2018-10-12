# Baseball Workbench
Baseball Workbench is an upcoming Web-based tool for Sabermetrics research.

The software for Baseball Workbench will be open-source, and will integrate with freely available data sources.

The hosted tool will have associated infrastructure costs, but we may look to offset these with sponsors,
ads, or fees at some point.

## Release Date
Update: I haven't released a hosted Alpha version of Baseball Workbench but I'll keep posting updates here! Feel free to follow along. Alpha access may be private to help control costs - if so, invite information will be posted to this README.

## Get development updates

If you're a GitHub user, you can "Watch" this project to get updates.

You can also check out the content on the [GitHub Wiki](https://github.com/bryantrobbins/baseball/wiki).

## Contributing

There are many ways you can contribute to Baseball Workbench!

Check out the Issues tab here on GitHub for work that is planned.

If you are a programmer (or want to try your hand at it!), check out the various code throughout the project and contribute enhancements:

* There is Python code in shared/, api/api.py, and worker/service.py
* There is R code in worker/service.py (this will move into a separate file soon!)
* Groovy is used in the worker/extract/download.groovy script (but may be changed to Python in the future for consistency)

If you know or want to learn AWS concepts, you can check out the infra folder, which uses AWS CloudFormation to define the hosted
version of the app.

If you are interested or experienced with baseball datasets such as the Lahman Database and Retrosheet Game Logs, you can check out
the data extraction script in worker/extract and the datasource metadata files in shared/btr3baseball/datasource. Both of these
are fairly easy to follow, and we will need a lot of work in these areas to integrate with interesting datasets.

Finally, once the hosted app is live for Alpha, you can contribute by logging Issues in the Issues tab for bugs you find and 
features you would like to see.

## Contact

If you have any questions about the Baseball Workbench, you can contact Bryan at bryantrobbins@gmail.com.
