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