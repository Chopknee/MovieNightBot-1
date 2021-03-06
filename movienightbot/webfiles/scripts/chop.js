
var Math2 = new math2();
var sVector3 = new Vector3();
var Utility = new _Utility();

function math2() {
	this.Lerp = function(value1, value2, a) {
		return value1 + (value2 - value1) * a;
	}

	this.LerpClamped = function(value1, value2, a) {
		a = a < 0 ? 0 : a;
		a = a > 1 ? 1 : a;
		return value1 + (value2 - value1) * a;
	}
}

function Vector3() {
	this.x = 0;
	this.y = 0;
	this.z = 0;

	this.Set = function(x, y, z) {
		this.x = x;
		this.y = y;
		this.z = z;
	}

	this.Add = function(other) {
		this.x += other.x;
		this.y += other.y;
		this.z += other.z;
	}

	this.Lerp = function(vector1, vector2, a) {
		let newVector = new Vector3();
		newVector.x = Math2.Lerp(vector1.x, vector2.x, a);
		newVector.y = Math2.Lerp(vector1.y, vector2.y, a);
		newVector.z = Math2.Lerp(vector1.z, vector2.z, a);
		return newVector;
	}

	this.Scale = function(scalar) {
		this.x *= scalar;
		this.y *= scalar;
		this.z *= scalar;
	}

	this.RGB = function() {
		return "rgb(" + this.x + "," + this.y + "," + this.z + ")";
	}

	this.ToString = function() {
		return "(" + this.x + "," + this.y + "," + this.z + ")";
	}
}

function _Utility() {

	this.CharIsNumber = function(char) {
		return char == '0' || char == '1' || char == '2' || char == '3' || char == '4' || char == '5' || char == '6' || char == '7' || char == '8' || char == '9';
	}
}