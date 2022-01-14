// source: engine.proto
/**
 * @fileoverview
 * @enhanceable
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!

goog.provide('proto.evomorph.StartRequest');

goog.require('jspb.BinaryReader');
goog.require('jspb.BinaryWriter');
goog.require('jspb.Message');

/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.evomorph.StartRequest = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.evomorph.StartRequest.repeatedFields_, null);
};
goog.inherits(proto.evomorph.StartRequest, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.evomorph.StartRequest.displayName = 'proto.evomorph.StartRequest';
}

/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.evomorph.StartRequest.repeatedFields_ = [1];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.evomorph.StartRequest.prototype.toObject = function(opt_includeInstance) {
  return proto.evomorph.StartRequest.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.evomorph.StartRequest} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.evomorph.StartRequest.toObject = function(includeInstance, msg) {
  var f, obj = {
    modelsList: (f = jspb.Message.getRepeatedField(msg, 1)) == null ? undefined : f,
    replicates: jspb.Message.getFieldWithDefault(msg, 2, 0),
    out: jspb.Message.getFieldWithDefault(msg, 3, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.evomorph.StartRequest}
 */
proto.evomorph.StartRequest.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.evomorph.StartRequest;
  return proto.evomorph.StartRequest.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.evomorph.StartRequest} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.evomorph.StartRequest}
 */
proto.evomorph.StartRequest.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.addModels(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readUint32());
      msg.setReplicates(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setOut(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.evomorph.StartRequest.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.evomorph.StartRequest.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.evomorph.StartRequest} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.evomorph.StartRequest.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getModelsList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      1,
      f
    );
  }
  f = message.getReplicates();
  if (f !== 0) {
    writer.writeUint32(
      2,
      f
    );
  }
  f = message.getOut();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
};


/**
 * repeated string models = 1;
 * @return {!Array<string>}
 */
proto.evomorph.StartRequest.prototype.getModelsList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 1));
};


/**
 * @param {!Array<string>} value
 * @return {!proto.evomorph.StartRequest} returns this
 */
proto.evomorph.StartRequest.prototype.setModelsList = function(value) {
  return jspb.Message.setField(this, 1, value || []);
};


/**
 * @param {string} value
 * @param {number=} opt_index
 * @return {!proto.evomorph.StartRequest} returns this
 */
proto.evomorph.StartRequest.prototype.addModels = function(value, opt_index) {
  return jspb.Message.addToRepeatedField(this, 1, value, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.evomorph.StartRequest} returns this
 */
proto.evomorph.StartRequest.prototype.clearModelsList = function() {
  return this.setModelsList([]);
};


/**
 * optional uint32 replicates = 2;
 * @return {number}
 */
proto.evomorph.StartRequest.prototype.getReplicates = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/**
 * @param {number} value
 * @return {!proto.evomorph.StartRequest} returns this
 */
proto.evomorph.StartRequest.prototype.setReplicates = function(value) {
  return jspb.Message.setProto3IntField(this, 2, value);
};


/**
 * optional string out = 3;
 * @return {string}
 */
proto.evomorph.StartRequest.prototype.getOut = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.evomorph.StartRequest} returns this
 */
proto.evomorph.StartRequest.prototype.setOut = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


