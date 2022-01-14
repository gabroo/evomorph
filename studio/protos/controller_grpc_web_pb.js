/**
 * @fileoverview gRPC-Web generated client stub for evomorph
 * @enhanceable
 * @public
 */

// GENERATED CODE -- DO NOT EDIT!


/* eslint-disable */
// @ts-nocheck


goog.provide('proto.evomorph.ControllerClient');
goog.provide('proto.evomorph.ControllerPromiseClient');

goog.require('grpc.web.MethodDescriptor');
goog.require('grpc.web.MethodType');
goog.require('grpc.web.GrpcWebClientBase');
goog.require('grpc.web.AbstractClientBase');
goog.require('grpc.web.ClientReadableStream');
goog.require('grpc.web.RpcError');
goog.require('proto.evomorph.Frame');
goog.require('proto.evomorph.Progress');
goog.require('proto.evomorph.RunReply');
goog.require('proto.evomorph.RunRequest');
goog.require('proto.evomorph.Simulation');
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
proto.evomorph.ControllerClient =
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
proto.evomorph.ControllerPromiseClient =
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
 *   !proto.evomorph.RunRequest,
 *   !proto.evomorph.RunReply>}
 */
const methodDescriptor_Controller_Run = new grpc.web.MethodDescriptor(
  '/evomorph.Controller/Run',
  grpc.web.MethodType.UNARY,
  proto.evomorph.RunRequest,
  proto.evomorph.RunReply,
  /**
   * @param {!proto.evomorph.RunRequest} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.evomorph.RunReply.deserializeBinary
);


/**
 * @param {!proto.evomorph.RunRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.RpcError, ?proto.evomorph.RunReply)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.evomorph.RunReply>|undefined}
 *     The XHR Node Readable Stream
 */
proto.evomorph.ControllerClient.prototype.run =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/evomorph.Controller/Run',
      request,
      metadata || {},
      methodDescriptor_Controller_Run,
      callback);
};


/**
 * @param {!proto.evomorph.RunRequest} request The
 *     request proto
 * @param {?Object<string, string>=} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.evomorph.RunReply>}
 *     Promise that resolves to the response
 */
proto.evomorph.ControllerPromiseClient.prototype.run =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/evomorph.Controller/Run',
      request,
      metadata || {},
      methodDescriptor_Controller_Run);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.evomorph.Simulation,
 *   !proto.evomorph.Status>}
 */
const methodDescriptor_Controller_Pause = new grpc.web.MethodDescriptor(
  '/evomorph.Controller/Pause',
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
proto.evomorph.ControllerClient.prototype.pause =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/evomorph.Controller/Pause',
      request,
      metadata || {},
      methodDescriptor_Controller_Pause,
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
proto.evomorph.ControllerPromiseClient.prototype.pause =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/evomorph.Controller/Pause',
      request,
      metadata || {},
      methodDescriptor_Controller_Pause);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.evomorph.Simulation,
 *   !proto.evomorph.Status>}
 */
const methodDescriptor_Controller_Resume = new grpc.web.MethodDescriptor(
  '/evomorph.Controller/Resume',
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
proto.evomorph.ControllerClient.prototype.resume =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/evomorph.Controller/Resume',
      request,
      metadata || {},
      methodDescriptor_Controller_Resume,
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
proto.evomorph.ControllerPromiseClient.prototype.resume =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/evomorph.Controller/Resume',
      request,
      metadata || {},
      methodDescriptor_Controller_Resume);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.evomorph.Simulation,
 *   !proto.evomorph.Status>}
 */
const methodDescriptor_Controller_Cancel = new grpc.web.MethodDescriptor(
  '/evomorph.Controller/Cancel',
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
proto.evomorph.ControllerClient.prototype.cancel =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/evomorph.Controller/Cancel',
      request,
      metadata || {},
      methodDescriptor_Controller_Cancel,
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
proto.evomorph.ControllerPromiseClient.prototype.cancel =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/evomorph.Controller/Cancel',
      request,
      metadata || {},
      methodDescriptor_Controller_Cancel);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.evomorph.Simulation,
 *   !proto.evomorph.Status>}
 */
const methodDescriptor_Controller_GetStatus = new grpc.web.MethodDescriptor(
  '/evomorph.Controller/GetStatus',
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
proto.evomorph.ControllerClient.prototype.getStatus =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/evomorph.Controller/GetStatus',
      request,
      metadata || {},
      methodDescriptor_Controller_GetStatus,
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
proto.evomorph.ControllerPromiseClient.prototype.getStatus =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/evomorph.Controller/GetStatus',
      request,
      metadata || {},
      methodDescriptor_Controller_GetStatus);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.evomorph.Simulation,
 *   !proto.evomorph.Progress>}
 */
const methodDescriptor_Controller_GetProgress = new grpc.web.MethodDescriptor(
  '/evomorph.Controller/GetProgress',
  grpc.web.MethodType.UNARY,
  proto.evomorph.Simulation,
  proto.evomorph.Progress,
  /**
   * @param {!proto.evomorph.Simulation} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.evomorph.Progress.deserializeBinary
);


/**
 * @param {!proto.evomorph.Simulation} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.RpcError, ?proto.evomorph.Progress)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.evomorph.Progress>|undefined}
 *     The XHR Node Readable Stream
 */
proto.evomorph.ControllerClient.prototype.getProgress =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/evomorph.Controller/GetProgress',
      request,
      metadata || {},
      methodDescriptor_Controller_GetProgress,
      callback);
};


/**
 * @param {!proto.evomorph.Simulation} request The
 *     request proto
 * @param {?Object<string, string>=} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.evomorph.Progress>}
 *     Promise that resolves to the response
 */
proto.evomorph.ControllerPromiseClient.prototype.getProgress =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/evomorph.Controller/GetProgress',
      request,
      metadata || {},
      methodDescriptor_Controller_GetProgress);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.evomorph.Simulation,
 *   !proto.evomorph.Frame>}
 */
const methodDescriptor_Controller_GetPictures = new grpc.web.MethodDescriptor(
  '/evomorph.Controller/GetPictures',
  grpc.web.MethodType.SERVER_STREAMING,
  proto.evomorph.Simulation,
  proto.evomorph.Frame,
  /**
   * @param {!proto.evomorph.Simulation} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.evomorph.Frame.deserializeBinary
);


/**
 * @param {!proto.evomorph.Simulation} request The request proto
 * @param {?Object<string, string>=} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.evomorph.Frame>}
 *     The XHR Node Readable Stream
 */
proto.evomorph.ControllerClient.prototype.getPictures =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/evomorph.Controller/GetPictures',
      request,
      metadata || {},
      methodDescriptor_Controller_GetPictures);
};


/**
 * @param {!proto.evomorph.Simulation} request The request proto
 * @param {?Object<string, string>=} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.evomorph.Frame>}
 *     The XHR Node Readable Stream
 */
proto.evomorph.ControllerPromiseClient.prototype.getPictures =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/evomorph.Controller/GetPictures',
      request,
      metadata || {},
      methodDescriptor_Controller_GetPictures);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.evomorph.Simulation,
 *   !proto.evomorph.Frame>}
 */
const methodDescriptor_Controller_GetStructures = new grpc.web.MethodDescriptor(
  '/evomorph.Controller/GetStructures',
  grpc.web.MethodType.SERVER_STREAMING,
  proto.evomorph.Simulation,
  proto.evomorph.Frame,
  /**
   * @param {!proto.evomorph.Simulation} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.evomorph.Frame.deserializeBinary
);


/**
 * @param {!proto.evomorph.Simulation} request The request proto
 * @param {?Object<string, string>=} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.evomorph.Frame>}
 *     The XHR Node Readable Stream
 */
proto.evomorph.ControllerClient.prototype.getStructures =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/evomorph.Controller/GetStructures',
      request,
      metadata || {},
      methodDescriptor_Controller_GetStructures);
};


/**
 * @param {!proto.evomorph.Simulation} request The request proto
 * @param {?Object<string, string>=} metadata User defined
 *     call metadata
 * @return {!grpc.web.ClientReadableStream<!proto.evomorph.Frame>}
 *     The XHR Node Readable Stream
 */
proto.evomorph.ControllerPromiseClient.prototype.getStructures =
    function(request, metadata) {
  return this.client_.serverStreaming(this.hostname_ +
      '/evomorph.Controller/GetStructures',
      request,
      metadata || {},
      methodDescriptor_Controller_GetStructures);
};


}); // goog.scope

