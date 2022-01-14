/**
 * @fileoverview gRPC-Web generated client stub for evomorph
 * @enhanceable
 * @public
 */

// GENERATED CODE -- DO NOT EDIT!


/* eslint-disable */
// @ts-nocheck


goog.provide('proto.evomorph.EngineClient');
goog.provide('proto.evomorph.EnginePromiseClient');

goog.require('grpc.web.MethodDescriptor');
goog.require('grpc.web.MethodType');
goog.require('grpc.web.GrpcWebClientBase');
goog.require('grpc.web.AbstractClientBase');
goog.require('grpc.web.ClientReadableStream');
goog.require('grpc.web.RpcError');
goog.require('proto.evomorph.Simulation');
goog.require('proto.evomorph.StartReply');
goog.require('proto.evomorph.StartRequest');
goog.require('proto.evomorph.Status');

goog.requireType('grpc.web.ClientOptions');



goog.scope(function() {

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?grpc.web.ClientOptions} options
 * @constructor
 * @struct
 * @final
 */
proto.evomorph.EngineClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options.format = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

};


/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?grpc.web.ClientOptions} options
 * @constructor
 * @struct
 * @final
 */
proto.evomorph.EnginePromiseClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options.format = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.evomorph.StartRequest,
 *   !proto.evomorph.StartReply>}
 */
const methodDescriptor_Engine_Start = new grpc.web.MethodDescriptor(
  '/evomorph.Engine/Start',
  grpc.web.MethodType.UNARY,
  proto.evomorph.StartRequest,
  proto.evomorph.StartReply,
  /**
   * @param {!proto.evomorph.StartRequest} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.evomorph.StartReply.deserializeBinary
);


/**
 * @param {!proto.evomorph.StartRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.RpcError, ?proto.evomorph.StartReply)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.evomorph.StartReply>|undefined}
 *     The XHR Node Readable Stream
 */
proto.evomorph.EngineClient.prototype.start =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/evomorph.Engine/Start',
      request,
      metadata || {},
      methodDescriptor_Engine_Start,
      callback);
};


/**
 * @param {!proto.evomorph.StartRequest} request The
 *     request proto
 * @param {?Object<string, string>=} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.evomorph.StartReply>}
 *     Promise that resolves to the response
 */
proto.evomorph.EnginePromiseClient.prototype.start =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/evomorph.Engine/Start',
      request,
      metadata || {},
      methodDescriptor_Engine_Start);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.evomorph.Simulation,
 *   !proto.evomorph.Status>}
 */
const methodDescriptor_Engine_Stop = new grpc.web.MethodDescriptor(
  '/evomorph.Engine/Stop',
  grpc.web.MethodType.UNARY,
  proto.evomorph.Simulation,
  proto.evomorph.Status,
  /**
   * @param {!proto.evomorph.Simulation} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.evomorph.Status.deserializeBinary
);


/**
 * @param {!proto.evomorph.Simulation} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.RpcError, ?proto.evomorph.Status)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.evomorph.Status>|undefined}
 *     The XHR Node Readable Stream
 */
proto.evomorph.EngineClient.prototype.stop =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/evomorph.Engine/Stop',
      request,
      metadata || {},
      methodDescriptor_Engine_Stop,
      callback);
};


/**
 * @param {!proto.evomorph.Simulation} request The
 *     request proto
 * @param {?Object<string, string>=} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.evomorph.Status>}
 *     Promise that resolves to the response
 */
proto.evomorph.EnginePromiseClient.prototype.stop =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/evomorph.Engine/Stop',
      request,
      metadata || {},
      methodDescriptor_Engine_Stop);
};


}); // goog.scope

