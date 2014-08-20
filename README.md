Smarter Complete
================

Apply machine learning and language processing to create smarter auto complete
suggestions when programming

Introduction
------------

This is an experimental project with the following goal(s):

1. To determine whether machine learning and language processing techniques can
be used to improve programmer efficiency by automatically identifying
frequently repeated code snippets from a large body of code and
(intelligently) proposing those snippets in typical auto-complete situations.
2. There's only one goal right now.

Target
------

The initial target editor is Sublime Text. Sublime Text is a popular editor
that exposes hooks into the auto-complete mechanism. Those hooks are easiest
to implement in Python. The target language for auto-completion is Javascript.
Javascript has been selected as it is a popular language, syntactically
relatively simple but (to the author at least) verbose, repetitive and ripe
for rich auto-complete suggestions.

Motivation
----------

Several factors are motivating this experiment.

1. Anecdotally, the author estimates that 99.5-99.9% of the time spent
programming is wasteful and inefficient. The mind's ability to imagine the
solution to a programming problem or write the next line is probably only
0.5-0.1% of the time it takes to actually transcribe, correct and test the
code. This only gets worse as programmers have to work with more complex
systems, reference documentation more frequently etc.

2. Recently, the author crafted a very large body of Javascript code in a
node.js based RESTful API. While modern frameworks allow for a much higher
level of abstraction, the act of transcribing code line by line was very
reminiscient of programming BASIC on a Commodore PET in 1979. Depressing.

3. While this is not true for all programmers, a couple of friends have
identified that a lot of "average" programming these days involves simply
copying and pasting code from one place to another, adjusting some variables
and moving on. Similarly depressing.

4. I was looking for a project to try out some new (to me) technologies.

Quantification
--------------

It's important to be able to measure the usefulness of this experiment. We're
going to measure usefulness in terms of getting the code that we expect in the
shortest possible time, or the fewest number of keypresses.

The code here represents a fragment that I felt like I wrote several times
each day for a period of two years:

```javascript
var async = require('async')
	, _ = require('underscore')
	;

function Target () {
	var self = this;
	self.invocations = 0;
}

Target.prototype.fibonacci = function(n, cb) {
	var self = this;
	self.invocations++;

	if (n < 1 || n > 100) return cb(new Error('Number out of range'));
	if (n === 1 || n === 2) return 1;

	async.auto({
		first : function (firstCallback) {
			self.fibonacci(n-1, firstCallback);
		},
		second : function (secondCallback) {
			self.fibonacci(n-2, secondCallback);
		}
	}, function (err, r) {
		if (err) return cb(err);
		cb(null, r.first + r.second);
	});
};
```

That's ~585 bytes which we can assume is 585 keypresses if we give ourselves
the benefit of the doubt and assume we can enter it perfectly correctly,
beginning to end, in one go.

Of course, in all programming there are idioms that machine learning should be
able to identify and take advantage of without language specific training. For
example, after examining a large body of code, the ML system should know that
require statements often come at the top of most node.js files, that async and
underscore are popular libraries, that typing "var _ " is extremely likely to
be followed by " = requrie('underscore')", that if we have an anoynmous
function at the end of our async.auto the first line is very likely to be
passing errors back up the callback chain, etc.

Having said that, we may follow a different coding style or we may not use
these libraries but instead use others and the ML system should be able to
take into account those differences and adapt to be efficient for each user.


